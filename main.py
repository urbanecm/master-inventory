import requests

requests.utils.default_user_agent = lambda: "master-invertory-bot (no webpage, martin.urbanec@wikimedia.cz)"

words = ['{{přesunout', '{{přejmenovat', '{{upravit', '{{cleanup', '{{pravopis', '{{NPOV', '{{Neutralita', '{{POV', '{{kategorizovat', '{{neověřeno', '{{bez zdrojů',  '{{ověřitelnost', '{{ověřit', '{{neozdrojováno', '{{reference', '{{pracuje se']
words_count = []
for word in words: words_count.append(0)

endswitch = ['|', '}}']

def request(rew_id):
    payload = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "revids": rew_id,
            "rvprop": "content"
        }
    request = requests.get("https://cs.wikipedia.org/w/api.php", params=payload)
    request = request.json()

    return request

def compare(new, old=False):
    if old != False:
        for word in range(len(words)):
            for switch in endswitch:
                if (words[word] + switch in new and words[word] + switch not in old) or ("{{" + words[word][2].upper() + words[word][3:] + switch in new and "{{" + words[word][2].upper() + words[word][3:] + switch not in old):
                    words_count[word] += 1
    else:
        for word in range(len(words)):
            for switch in endswitch:
                if (words[word] + switch in new or "{{" + words[word][2].upper() + words[word][3:] + switch in new):
                    words_count[word] += 1
        
def main():

    with open('revisions.txt', 'r') as f:
        f.readline() #skip first
        
        for line in f:
            tmp = f.readline().split('\t')
            if tmp[1] != '0':
                new = str(request(tmp[0]))
                compare(new)
            else:
                old = str(request(tmp[1]))
                new = str(request(tmp[0]))
                compare(new, old)
            print(words)
            print(words_count)
            
    with open('res.txt', 'w') as f:
        f.writeline(words)
        f.writeline(words_count)
            

if __name__ == "__main__":
    main()
