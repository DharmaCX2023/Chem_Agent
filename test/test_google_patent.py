import requests
main_url="https://patents.google.com/"
params="?assignee=Roche&after=priority:20110602&type=PATENT&num=100"

res=requests.get("https://patents.google.com/xhr/query?url=assignee%3DRoche%26after%3Dpriority%3A20110602%26type%3DPATENT%26num%3D100&exp=")
main_data=res.json()
data=main_data['results']['cluster']

for i in range(len(data[0]['result'])):
    num=data[0]['result'][i]['patent']['publication_number']
    print(num)
    print(main_url+"patent/"+num+"/en"+params)