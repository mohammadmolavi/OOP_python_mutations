import ast
import astor  # Install with `pip install astor`
import os


# Mutation Transformer Class
class MutationTransformer(ast.NodeTransformer):
    def __init__(self, mutation_type):
        self.mutation_type = mutation_type

    def visit_FunctionDef(self, node):
        # Handle method-related mutations
        if self.mutation_type == "PMD":  # Polymorphic Method Deletion
            if node.name == "make_sound":
                return None  # Delete the function

        elif self.mutation_type == "OMD":  # Overriding Method Deletion
            if node.name == "get_info":
                return None  # Delete the overridden method

        elif self.mutation_type == "IOD":  # Incorrect Method Overriding
            if node.name == "make_sound":
                # Change the method signature
                node.args.args.append(ast.arg(arg="loud", annotation=None))
                # node.body = [
                #     ast.Return(
                #         value=ast.IfExp(
                #             test=ast.Name(id="loud", ctx=ast.Load()),
                #             body=ast.Str(s="Loud Bark!"),
                #             orelse=ast.Str(s="Bark!"),
                #         )
                #     )
                # ]
                node.body = [
                    ast.Return(
                        value=ast.IfExp(
                            test=ast.Name(id="loud", ctx=ast.Load()),
                            body=ast.Constant(value="Loud Bark!"),
                            orelse=ast.Constant(value="Bark!"),
                        )
                    )
                ]

        elif self.mutation_type == "ISI":  # Insert Super Invocation
            if node.name == "make_sound":
                # super_call = ast.Expr(
                #     value=ast.Call(
                #         func=ast.Attribute(
                #             value=ast.Call(func=ast.Name(id="super", ctx=ast.Load()), args=[], keywords=[]),
                #             attr="make_sound",
                #             ctx=ast.Load(),
                #         ),
                #         args=[],
                #         keywords=[],
                #     )
                # )
                super_call = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(func=ast.Name(id="super", ctx=ast.Load()), args=[], keywords=[]),
                            attr="make_sound",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[],
                    )
                )
                node.body.insert(0, super_call)

        elif self.mutation_type == "OAC":  # Argument Change
            if node.name == "get_info":
                # Add a new argument to the method
                node.args.args.append(ast.arg(arg="detailed", annotation=None))
                # node.body = [
                #     ast.If(
                #         test=ast.Name(id="detailed", ctx=ast.Load()),
                #         body=[
                #             ast.Return(
                #                 value=ast.Str(s="Detailed information provided.")
                #             )
                #         ],
                #         orelse=[
                #             ast.Return(
                #                 value=ast.Str(s="Basic information provided.")
                #             )
                #         ],
                #     )
                # ]
                node.body = [
                    ast.If(
                        test=ast.Name(id="detailed", ctx=ast.Load()),
                        body=[
                            ast.Return(value=ast.Constant(value="Detailed information provided."))
                        ],
                        orelse=[
                            ast.Return(value=ast.Constant(value="Basic information provided."))
                        ],
                    )
                ]

        elif self.mutation_type == "PPD":  # Parameter Deletion
            if node.name == "__init__":
                if len(node.args.args) > 2:  # Ensure at least one parameter exists
                    node.args.args.pop(-1)  # Remove the last parameter

        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        # Handle class-related mutations
        if self.mutation_type == "IHI":  # Hiding a Method in Subclass
            if node.name == "Dog":
                # new_method = ast.FunctionDef(
                #     name="get_info",
                #     args=ast.arguments(
                #         posonlyargs=[], args=[ast.arg(arg="self", annotation=None)], vararg=None, kwarg=None, kwonlyargs=[], kw_defaults=[], defaults=[]
                #     ),
                #     body=[
                #         ast.Return(value=ast.Str(s="Hidden method in Dog")),
                #     ],
                #     decorator_list=[],
                # )
                new_method = ast.FunctionDef(
                    name="get_info",
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg="self", annotation=None)],
                        vararg=None,
                        kwarg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=[ast.Return(value=ast.Constant(value="Hidden method in Dog"))],
                    decorator_list=[],
                )
                node.body.append(new_method)

        elif self.mutation_type == "IHD":  # Hiding a Field in Subclass
            if node.name == "Dog":
                new_field = ast.Assign(
                    targets=[
                        ast.Attribute(value=ast.Name(id="self", ctx=ast.Load()), attr="name", ctx=ast.Store())
                    ],
                    value=ast.Constant(value="Hidden field in Dog"),
                )
                node.body.insert(0, new_field)

        elif self.mutation_type == "IPC":  # Change Parent Class
            if node.name == "Dog":
                node.bases = [ast.Name(id="object", ctx=ast.Load())]

        elif self.mutation_type == "PCD":  # Constructor Deletion
            node.body = [n for n in node.body if not isinstance(n, ast.FunctionDef) or n.name != "__init__"]

        elif self.mutation_type == "PCI":  # Constructor Inlining
            if node.name == "Dog":
                new_method = ast.FunctionDef(
                    name="set_info",
                    args=ast.arguments(
                        posonlyargs=[], args=[
                            ast.arg(arg="self", annotation=None),
                            ast.arg(arg="name", annotation=None),
                            ast.arg(arg="age", annotation=None),
                            ast.arg(arg="breed", annotation=None)
                        ], vararg=None, kwarg=None, kwonlyargs=[], kw_defaults=[], defaults=[]
                    ),
                    body=[
                        ast.Assign(
                            targets=[ast.Attribute(value=ast.Name(id="self", ctx=ast.Load()), attr="name", ctx=ast.Store())],
                            value=ast.Name(id="name", ctx=ast.Load()),
                        ),
                        ast.Assign(
                            targets=[ast.Attribute(value=ast.Name(id="self", ctx=ast.Load()), attr="age", ctx=ast.Store())],
                            value=ast.Name(id="age", ctx=ast.Load()),
                        ),
                        ast.Assign(
                            targets=[ast.Attribute(value=ast.Name(id="self", ctx=ast.Load()), attr="breed", ctx=ast.Store())],
                            value=ast.Name(id="breed", ctx=ast.Load()),
                        ),
                    ],
                    decorator_list=[],
                )
                node.body.append(new_method)

        return self.generic_visit(node)

    def visit_Attribute(self, node):
        # Handle encapsulation-related mutations
        if self.mutation_type == "AMC":  # Access Modifier Change
            if isinstance(node.value, ast.Name) and node.attr == "_age":
                node.attr = "age"
        return self.generic_visit(node)


# Function to apply a mutation
def apply_mutation(source_code, mutation_type):
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Apply the mutation using the transformer
    transformer = MutationTransformer(mutation_type)
    mutated_tree = transformer.visit(tree)

    # Return the mutated code as a string
    return astor.to_source(mutated_tree)


# Mutation Testing Script
def mutate_file(input_file, output_dir, mutations):
    # Read the source code from the input file
    with open(input_file, "r") as f:
        source_code = f.read()

    # Apply each mutation and save the result
    for mutation in mutations:
        mutated_code = apply_mutation(source_code, mutation)
        output_file = os.path.join(output_dir, f"mutated_{mutation}.py")
        with open(output_file, "w") as f:
            f.write(mutated_code)
        print(f"Mutation '{mutation}' applied and saved to: {output_file}")


# Example Usage
if __name__ == "__main__":
    # Path to the original source file
    input_file = "original_code.py"  # Replace with your file
    # Directory to save mutated files
    output_dir = "mutants"
    os.makedirs(output_dir, exist_ok=True)

    # List of mutations to apply
    mutations = ["AMC", "IHI", "IHD", "IOD", "ISI", "IPC", "PMD", "PPD", "PCI", "PCD", "OMD", "OAC"]

    # Perform the mutation testing
    mutate_file(input_file, output_dir, mutations)


#