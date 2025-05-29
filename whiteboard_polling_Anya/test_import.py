from cpp_module.filter import apply_filter_cpp

# Викликаємо функцію з переданими аргументами
result = apply_filter_cpp([0, 0, 0, 255], 1, 1, "invert")

# Виводимо результат
print(result)
