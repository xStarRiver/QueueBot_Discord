import json
import os

class data:
    def __init__(self, rtype):
        self.rtype = rtype
    
    def dirs(self):
        return os.listdir(f"json/{self.rtype}")
            
    def load(self, file_name):
        return json.load(open("json/%s/%s" % (self.rtype, file_name),'r'))

    def get(self, key):
        got = False
        for file_ in self.dirs():
            fdata = self.load(file_)
            if key in fdata.keys() and got == False:
                got = True
                return file_
        if got == False:
            return None

    def get_data(self, user):
        try:
            return self.load(self.get(user))[user]
        except:
            return None
            
    def new(self, num, user, data):
        with open(f"json/{self.rtype}/{self.rtype}_{num}.json",'w+') as f_data:
            json.dump({user: data}, f_data)

    def write(self, user, data):
        user = str(user)
        filename = self.get(user)
        if filename is not None:
            f_dict = self.load(filename)
            with open(f"json/{self.rtype}/{filename}",'w+') as f_data:
                f_dict[user] = data
                json.dump(f_dict, f_data)
        else:
            if self.dirs() == []:
                self.new("0", user, data)
            else:
                file = self.dirs()
                file.sort()
                f_dict = self.load(file[-1])
                if len(f_dict) < 10:
                    with open('json/{}/{}'.format(self.rtype,self.dirs()[-1]),'w+') as f_data:
                        f_dict[user] = data
                        json.dump(f_dict, f_data)
                        # xp_data.write(xp_dict)
                else: 
                    self.new(str(len(self.dirs())), user, data)
        
class setting:
    def __init__(self, key):
        self.key = key
        with open('json/config.json','r') as data:
            self.config = json.load(data)[key]
        
    def set(self,new_config):
        with open('json/config.json','r') as data:
            f_dict = json.load(data)
        with open("json/config.json",'w+') as f_data:
            f_dict[self.key] = new_config
            json.dump(f_dict, f_data)


        

class config:
    
    def get(self,key):
        with open('json/config.json','r') as data:
            return json.load(data)[key]
            
    def get_guild(self, guild):
        return data("guild").get_data(guild)
        
    def set_guild(self, guild, config_value):
        data("guild").write(guild, config_value)


def queue(user):
    got = False
    queues = data("queue")
    dirs = queues.dirs()
    dirs.sort()
    for q in dirs:
        for key, datas in queues.load(q).items():
            if datas["userid"] == user.id:
                got = True
    print(dirs)
    try:
        position = int(list(queues.load(dirs[-1]).keys())[-1])
    except:
        position = 0
    print(position)
    if not got:
        position += 1
        datas = {"userid":user.id,"user":user.name+"#"+user.discriminator}
        if dirs == []:
            queues.new("0", position, datas)
        else:
            dirs.sort()
            f_dict = queues.load(dirs[-1])
            if len(f_dict) < 80:
                with open('json/queue/{}'.format(dirs[-1]),'w+') as f_data:
                    f_dict[position] = datas
                    json.dump(f_dict, f_data)
            else: 
                queues.new(str(len(queues.dirs())), position, datas)


def number_emoji(number):
    data = {1: ':one:', 2: ':two:', 3: ':three:', 4: ':four:', 5: ':five:', \
            6: ':six:', 7: ':seven: ', 8: ':eight:', 9: ':nine:', 10: ':keycap_ten:'}
    return data[number]
        
def help_data():
    with open('json/help.json','r') as data:
        return json.load(data)