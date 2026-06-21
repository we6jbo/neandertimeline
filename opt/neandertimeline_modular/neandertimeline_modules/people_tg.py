SUPPORTING_OLD_WORLD_TG_PEOPLE=[
{'region':'British Isles','name':'Edward McCabe','birth':'Mar 1861, Scotland','death':'1900, Pennsylvania','location':'Scotland -> Pennsylvania','tg':'TG628417'},
{'region':'British Isles','name':'Sarah McAvoy','birth':'13 Apr 1862, Cockermouth, Cumberland, England','death':'1934, Pennsylvania','location':'England -> Pennsylvania','tg':'TG628417'},
{'region':'British Isles','name':'James McCabe','birth':'About 1840, Ireland','death':'','location':'Ireland','tg':'TG307645'},
{'region':'British Isles','name':'James McAvoy','birth':'17 Mar 1833, Ireland','death':'24 Oct 1906, Pennsylvania','location':'Ireland -> Pennsylvania','tg':'TG918273 / TG891052'},
{'region':'British Isles','name':'John Sloan','birth':'May 1820, County Down, Ireland','death':'1 Aug 1900, Pennsylvania','location':'County Down -> Pennsylvania','tg':'TG540918'},
{'region':'German-speaking Central Europe','name':'Johann Jacob Friedrich Huber','birth':'11 Jan 1804, Attlisberg, Waldshut, Baden-Württemberg, Germany','death':'7 May 1877, Attlisberg, Germany','location':'Baden-Württemberg, Germany','tg':'TG182976'},
{'region':'German-speaking Central Europe','name':'Frederika Regkukel','birth':'1800, Attlisberg, Waldshut, Baden-Württemberg, Germany','death':'1830, Attlisberg, Germany','location':'Baden-Württemberg, Germany','tg':'TG182976'},
{'region':'Prussia / Pomerania / Schleswig-Holstein','name':'William John Ludwig Sclorf','birth':'21 Jul 1867, Pomerania, Prussia','death':'1937, Wisconsin','location':'Pomerania, Prussia -> Wisconsin','tg':'TG742018'},
{'region':'Prussia / Pomerania / Schleswig-Holstein','name':'Mary Johannsen','birth':'28 Nov 1868, Tondern, Schleswig-Holstein, Deutschland','death':'1951, Wisconsin','location':'Schleswig-Holstein -> Wisconsin','tg':'TG742018'},
{'region':'Prussia / Pomerania / Schleswig-Holstein','name':'August Friedrich Hedtke','birth':'23 Aug 1847, Alt Paleschken, Danzig, West Prussia','death':'31 Jan 1918, Minnesota','location':'West Prussia -> Minnesota','tg':'TG903148'},
{'region':'Prussia / Pomerania / Schleswig-Holstein','name':'Amelia Carolina Luedtke','birth':'Feb 1850, Pomerania, Prussia','death':'24 Apr 1925, Minnesota','location':'Pomerania -> Minnesota','tg':'TG903148 / TG610982'},
{'region':'Black Sea / Odessa / Kherson region','name':'Josef Kiehlbauch','birth':'1 Jan 1850, Neuberg, Russia','death':'14 Sep 1908, Chicago, Illinois','location':'Neuberg, Russia -> Illinois','tg':'TG472690'},
{'region':'Black Sea / Odessa / Kherson region','name':'Barbara Beck','birth':'22 Jan 1850, Lustdorf, Russia','death':'15 Jul 1923, South Dakota','location':'Lustdorf, Russia -> South Dakota','tg':'TG472690'},
{'region':'Black Sea / Odessa / Kherson region','name':'Joseph Sr. Kiehlbauch','birth':'22 Jan 1826, Neuberg, Cherson Province, New Odessa, Russia','death':'29 May 1902, South Dakota','location':'Cherson/New Odessa -> South Dakota','tg':'TG274361'},
{'region':'Black Sea / Odessa / Kherson region','name':'Johanna Knoepfle','birth':'25 Jul 1824, Alexanderhilf, Odessa, Russia','death':'21 Apr 1910, North Dakota','location':'Odessa, Russia -> North Dakota','tg':'TG274361'},
{'region':'Black Sea / Odessa / Kherson region','name':'Constantin Beck','birth':'16 May 1812, Wuerttemberg, Germany','death':'4 Aug 1857, Luftsdorf, Odessa','location':'Wuerttemberg -> Odessa','tg':'TG835097'},
{'region':'Black Sea / Odessa / Kherson region','name':'Barbara Maier/Beck','birth':'18 May 1811','death':'11 Jun 1856, Odessa, Kherson, Russia','location':'Odessa / Kherson, Russia','tg':'TG835097'},]
class PeopleTGModule:
    module_name='people_tg'
    def __init__(self): self.supporting=SUPPORTING_OLD_WORLD_TG_PEOPLE
    def get_people_for_region(self,region): return [p for p in self.supporting if p['region']==region]
    def get_reference_marks(self): return self.supporting
    def text_lines_for_region(self,region,limit=12):
        out=[]
        for p in self.get_people_for_region(region)[:limit]:
            line=f"{p['name']} | B: {p['birth']}"
            if p['death']: line += f" | D: {p['death']}"
            line += f" | Place: {p['location']} | {p['tg']}"; out.append(line)
        return out
    def export_for_ai(self): return {'module':self.module_name,'supporting_old_world_tg_people':self.supporting}

