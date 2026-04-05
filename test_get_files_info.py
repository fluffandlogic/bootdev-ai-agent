from functions.get_files_info import get_files_info

print(get_files_info("calculator", "."))
print("\n")

print(get_files_info("calculator", "pkg"))
print("\n")

print(get_files_info("calculator", "/bin"))
print("\n")

print(get_files_info("calculator", "../"))
print("\n")