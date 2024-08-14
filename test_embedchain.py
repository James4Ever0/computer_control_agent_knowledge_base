from lib import EmbedApp
import subprocess


def get_dir_size(dirpath: str):
    cmdlist = [
        "bash",
        "-c",
        "du -c " + dirpath + " | tail --lines 1 | awk '{print $1}'",
    ]
    dirsize = subprocess.check_output(cmdlist, encoding="utf-8")
    ret = int(dirsize.strip())
    return ret


def test():
    embedApp = EmbedApp(config_path="secret.test_embedchain_config.yaml")
    embedApp.add("https://baai-agents.github.io/Cradle/")
    # check the size of the directory, see if it is the same
    dirPath = "db"
    actual_size = get_dir_size(dirPath)
    expected_size = 1940
    assert (
        actual_size == expected_size
    ), f"[-] Directory size mismatch: {actual_size} != {expected_size} (expected)"
    answer = embedApp.query("How is Cradle different from other projects?")
    assert (
        type(answer) == str
    ), f"[-] Invalid answer type '{type(answer)}':\nAnswer: {answer}"
    print("[+] Test passed")


if __name__ == "__main__":
    test()
