# json2md.py - quick script to generate Markdown documents for P-SSCRM practices and tasks defined in p-sscrm-1_0.json
# This probably should take arguments, e.g. the json file, an optional practice or task name, a directory in which to store the results

import json
# q_columns = ['ID','Business Function','Security Practice','Activity','Maturity','Question','Guidance','Answer Option']                

def make_filename(id,name):
    return id.replace(".","_") + "_" + name.replace(" ","_").replace("/","_").lower()

def make_practice_markdown(p):
    result = ""
    result += "# " + p['id'] + " " + p['name'] + "\n"
    result += "\n"
    result += "## Description" + "\n"
    result += p['description'] + "\n"
    
    return result

def make_task_markdown(t):
    result = ""
    result += "# " + t['id'] + " " + t['name'] + "\n\n"
    result += "## Objective" +"\n"
    result += t['objective'] + "\n\n"
    result += "## Definition" +"\n"
    result += t['definition'] + "\n"
    result += "## Questions" + "\n\n"
    for q in t['questions']:
        result += "### " + q['id'] + "\n\n"
        result += q['text'] + "\n\n"
        
    
    return result

def main():
    jfilename = "data/p-sscrm-1_0.json"
    j = json.load(open(jfilename))
    for g in j['groups']:
        print("Group: ", g['name'])
        for p in g['practices']:
            print("Practice: ", p['name'],p['id'], "filename = ","results/" + make_filename(p['id'],p['name']) + ".md")
            pfilename = make_filename(p['id'],p['name']) + ".md"
            markdown = make_practice_markdown(p)
            with open("results/" + pfilename,"w") as pf:
                pf.write(markdown)
                pf.write("## Tasks\n\n")
                for t in p['tasks']:
                    print("Task: ", t['name'],t['id'], "filename = ","results/" + make_filename(t['id'],t['name']) + ".md")
                    tfilename = make_filename(t['id'],t['name']) + ".md"
                    markdown = make_task_markdown(t)
                    with open("results/" + tfilename,"w") as pt:
                        pt.write(markdown)
                    # Add link to task in practice file
                    pf.write("[" + t['id'] + " " + t['name'] + "](" + tfilename + ")"+"\n\n")

if __name__ == '__main__':
    main()      
