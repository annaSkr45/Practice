// Polling-based Whiteboard client
const ROOM_ID = "room_6027"; // replace after gen_config
const API = "http://localhost:8000";
const FILTERS = ['blur', 'invert', 'MediumVioletRed', 'sepia'];

const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
let drawing = false;

let currentFilter = FILTERS[0]; // Початковий фільтр

const select = document.getElementById("filter-select");

// Додаємо фільтри до селекту
FILTERS.forEach(f => {
    const opt = document.createElement("option");
    opt.value = f;
    opt.textContent = f;
    select.appendChild(opt);
});

// Обробник кнопки Apply Filter
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("apply-filter").addEventListener("click", applyFilter);
});

async function applyFilter() {
  const { width, height } = canvas;
  
    // Додаємо білий фон під уже намальовані лінії
  ctx.save();
  ctx.globalCompositeOperation = "destination-over";
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.restore();

  const imgData = ctx.getImageData(0, 0, width, height);
  const dataArray = Array.from(imgData.data);

  const filterName = select.value; // Обраний фільтр

  console.log('Applying filter:', filterName);  // Перевірка в консолі

  // Відправляємо POST-запит на сервер
  const res = await fetch(`http://localhost:8000/filter/${ROOM_ID}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      image_data: dataArray,
      filter_name: filterName,
      width,
      height
    })
  });

  const json = await res.json();
  
  // Перевірка отриманих даних
  console.log(json);

  // Отримуємо нові пікселі та малюємо назад на Canvas
  const newData = new Uint8ClampedArray(json.image_data);
  ctx.putImageData(new ImageData(newData, width, height), 0, 0);
}

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => { drawing = false; ctx.beginPath(); });
canvas.addEventListener('mousemove', e => {
  if(!drawing) return;
  const rect = canvas.getBoundingClientRect();
  const cmd = { x: e.clientX - rect.left, y: e.clientY - rect.top, type: "line" };
  sendCommand(cmd);
  draw(cmd);
});

document.getElementById('refresh').onclick = poll;

function draw(cmd){
  ctx.lineTo(cmd.x, cmd.y);
  ctx.stroke();
}

async function sendCommand(cmd){
  await fetch(`${API}/draw/${ROOM_ID}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cmd)
  });
}

async function poll(){
  const res = await fetch(`${API}/draw/${ROOM_ID}`);
  const cmds = await res.json();
  ctx.clearRect(0,0,canvas.width,canvas.height);
  cmds.forEach(draw);
}

// initial data
poll();