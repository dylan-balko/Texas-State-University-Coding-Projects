class ClassGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.class_definition = []
        
    # Function to read data from text file
    def read_data_from_text(self):
        try:
            with open(self.filename, 'r') as file:
                data = file.read().strip()
            self.class_definition = [block.splitlines() for block in data.split("\n\n")]    
            return self.class_definition
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []
        except Exception as e:
            print(f"An error occured: {e}")
            return []

    #generates the class by indexing the lines of the class and reading them as class
    #name first line and class variables line 2 and on    
    def generate_class_from_file(self, class_definition):
        class_name_line = class_definition[0].split(":")
        class_name = class_name_line[0].strip()
        parent_class = class_name_line[1] if len(class_name_line) > 1 else None
        class_variables = class_definition[1:]

        if parent_class:
            class_code = f"class {class_name}({parent_class}):\n"
        else:
            class_code = f"class {class_name}:\n"
        
        #writes the instructor part of the class
        class_code += f"\t#Instructor\n"
        class_code += "\tdef __init__(self, {}):".format(", ".join(f"{variable}=None" for variable in class_variables))
        class_code += f"\n"
        if parent_class:
            class_code += "\t\tsuper().__init__(insert args here)\n"
        for variable in class_variables:
            class_code += f"\t\tself._{variable} = {variable}\n"
        class_code += f"\n"
        
        #writes the accessor methods or the "gets"
        for variable in class_variables:
            class_code += f"\t#Accessor for {variable}\n"
            class_code += f"\tdef get_{variable}(self):\n"
            class_code += f"\t\treturn self._{variable}\n\n"

        #write the mutator methods or the "sets"
        for variable in class_variables:
            class_code += f"\t#Mutator for {variable}\n"
            class_code += f"\tdef set_{variable}(self, {variable}):\n"
            class_code += f"\t\tself._{variable} = {variable}\n\n"

        return class_code

    def generate_all_classes(self):
        all_classes = ""
        for class_definition in self.class_definition:
            class_code = self.generate_class_from_file(class_definition)
            all_classes += class_code + "\n"
        return all_classes

    #writes the generated class into a file
    def write_class_to_py_file(self, filename):
        all_classes = self.generate_all_classes()
        if all_classes:
            with open(filename, 'w') as file:
                file.write(all_classes)
                print(f"Generated class succesfully written to {filename}.")

    #calls all the methods to read a class and write it to a .py file
    #without ever having to spend a lot of time writing and debugging typos
def main():
    generator = ClassGenerator("class_definition.txt")
    generator.read_data_from_text()
    generator.write_class_to_py_file("generated_class.py")

if __name__ == "__main__":
        main()
