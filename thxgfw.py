import base64
import sys
import requests


direct_list = "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/direct-list.txt"
direct_file = "direct-list.txt"

gfw_list = "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
gfw_file = "gfwlist.txt"


def gen_gfw_list(input_url, output_file):
    resp = requests.get(input_url)
    if not resp.ok:
        sys.exit(f"Get list code: {resp.status_code}")

    s = base64.b64decode(resp.text).decode()
    # print(s)
    with open(output_file, "w") as fw:
        for line in s.split("\n"):
            fw.write(f"{line}\n")


def gen_direct_list(input_url, output_file):
    resp = requests.get(input_url)
    if not resp.ok:
        sys.exit(f"Get list code: {resp.status_code}")

    domain = [
        "||mylocalhost.com",
        "||shengcaiyoushu.com",
        "||galaxy-future.com",
        "||scys.com",
    ]
    sub_domain = []
    regex_list = [
        "/.+\.com\.cn/",
        "/.+ac.cn/",
        "/.+acs.cn/",
        "/.+chaoxing.com/",
        "/.+edu.cn/",
        "/.+gov.cn/",
        "/.+net.cn/",
        "/.+sh.cn/",
    ]

    s = resp.text
    # print(s)
    for line in s.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("full:"):
            line = line[len("full:") :]
            line = f"|https://{line}"
            sub_domain.append(line)
        elif line.startswith("regexp:"):
            line = line[len("regexp:") :]
            line = line.rstrip("$")
            line = line.lstrip("^")
            line = f"/{line}/"
            regex_list.append(line)
        else:
            line = f"||{line}"
            domain.append(line)

    domain = list(sorted(domain))
    sub_domain = list(sorted(sub_domain))
    regex_list = list(sorted(regex_list))

    with open(output_file, "w") as fw:
        if regex_list:
            fw.write("! regex\n")
            for i in regex_list:
                fw.write(f"{i}\n")
            fw.write("\n")

        if sub_domain:
            fw.write("! subdomain\n")
            for i in sub_domain:
                fw.write(f"{i}\n")
            fw.write("\n")

        if domain:
            fw.write("! domain\n")
            for i in domain:
                fw.write(f"{i}\n")
            fw.write("\n")


if __name__ == "__main__":
    # gen_gfw_list(gfw_list, gfw_file)
    gen_direct_list(direct_list, direct_file)
