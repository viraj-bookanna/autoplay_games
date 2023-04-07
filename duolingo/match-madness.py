import subprocess,re,json,uiautomator2,asyncio,os,time
import xml.etree.ElementTree as ET
from googletrans import Translator

async def get_buttons():
    buttons = {
        'left': {},
        'right': {}
    }
    xml = client.dump_hierarchy()
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    for node in root.iter('node'):
        #print(node.attrib)
        #print(node.attrib['resource-id'], node.attrib['text'])
        skipBtns = ["NO THANKS", "CONTINUE", "END SESSION"]
        if node.attrib['text'] in skipBtns or node.attrib['resource-id'] in ["com.duolingo:id/matchMadnessStartChallenge", "com.duolingo:id/tabLeagues", "com.duolingo:id/rampUpFab"]:
            pos = re.search('\[(\d+),(\d+)\]\[(\d+),(\d+)\]', node.attrib['bounds'])
            pos = [round((int(pos[1])+int(pos[3]))/2), round((int(pos[2])+int(pos[4]))/2)]
            await tap_button(pos)
            return await get_buttons()
        elif node.attrib['resource-id'] == "com.duolingo:id/optionText" and node.attrib['enabled']:
            pos = re.search('\[(\d+),(\d+)\]\[(\d+),(\d+)\]', node.attrib['bounds'])
            pos = [round((int(pos[1])+int(pos[3]))/2), round((int(pos[2])+int(pos[4]))/2)]
            if pos[0] < 300:
                buttons['left'][node.attrib['text']] = {'coords': pos}
                continue
            buttons['right'][node.attrib['text']] = {'coords': pos}
        elif node.attrib['resource-id'] == "com.duolingo:id/optionText" and not node.attrib['enabled']:
            print('DISABLED BUTTON ----------->', node.attrib['text'], '<-----------')
    return buttons
async def tap_button(btn):
    try:
        client.click(*(btn['coords']))
        btn['clicked'] = True
    except:
        client.click(*btn)
async def tap_pair(btn1, btn2):
    await tap_button(btn1)
    await tap_button(btn2)
async def update(file_name, jdata):
    with open(file_name, 'w') as f:
        f.write(json.dumps(jdata, indent=4))
async def translate(txt, src):
    return t.translate(txt, src=src).text
async def purge(old, new):
    try:
        okeys = list(old['right'].keys())
        nkeys = list(new['right'].keys())
        for i in range(len(nkeys)):
            if okeys[i] != "null{}".format(i) and nkeys[i] == okeys[i] and old['right'][okeys[i]]['clicked']:
                new['right'] = {"null{}".format(i) if k == okeys[i] else k:v for k,v in new['right'].items()}
        return new
    except Exception as e:
        return new
async def main():
    unknown = {}
    try:
        last_check = 0
        buttons = {'left': {},'right': {}}
        swap = True
        while 1:
            if client.app_current()['package'] != "com.duolingo":
                client.app_start("com.duolingo", use_monkey=True)
                continue
            if last_check+60 < time.time():
                if not "com.pdanet" in client.app_list_running():
                    client.app_start("com.pdanet", use_monkey=True)
                    await asyncio.sleep(1)
                    client.app_start("com.duolingo", use_monkey=True)
                    os.system('start "PdaNetPC" "C:\Program Files (x86)\PdaNet for Android\PdaNetPC.exe"')
                    last_check = time.time()
            with open('translations.json', 'r') as f:
                tr = json.loads(f.read())
            # buttons = await get_buttons()
            # for button in buttons['right']:
            btbak = await get_buttons()
            buttons = await purge(buttons, btbak)
            try:
                last2 = list(btbak['right'].keys())[-2:]
            except:
                last2 = []
            swap = not swap
            for button in buttons['right']:
                if swap and button in last2:
                    continue
                if button in tr:
                    try:
                        b_right = buttons['right'][button]
                        b_left = buttons['left'][tr[button]]
                        print(button, "=>", tr[button])
                    except KeyError:
                        print('------> DIC-ERR:', button, "=>", tr[button])
                        continue
                    await tap_pair(b_right, b_left)
                elif not button.startswith("null"):
                    gtranslation = await translate(button, 'es')
                    if gtranslation in buttons['left']:
                        print(button, "=>", gtranslation)
                        await tap_pair(buttons['right'][button], buttons['left'][gtranslation])
                        tr[button] = gtranslation
                        await update('translations.json', tr)
                    else:
                        print('------> TR-ERR:', button, "=>", gtranslation)
                        unknown[button] = gtranslation
                        await update('unknown.json', unknown)
    except KeyboardInterrupt:
        exit()

client = uiautomator2.connect()
t = Translator()
asyncio.run(main())