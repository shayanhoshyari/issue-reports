load("@rules_uv//uv:pip.bzl", "pip_compile")
load("@rules_uv//uv:venv.bzl", "create_venv")

pip_compile(
    name = "requirements",
    requirements_in = "requirements.in",
    requirements_txt = "requirements.txt",
)

create_venv(
    name = "venv",
    destination_folder = ".venv",
    requirements_txt = "requirements.txt",
)