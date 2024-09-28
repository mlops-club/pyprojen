import platform


def make_cross_platform(command: str) -> str:
    if platform.system() != "Windows":
        return command

    return " && ".join(
        f"shx {subcommand.strip()}"
        if subcommand.strip().split()[0] in ["cat", "cp", "mkdir", "mv", "rm"]
        else subcommand.strip()
        for subcommand in command.split("&&")
    )
