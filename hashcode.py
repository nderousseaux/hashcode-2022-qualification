import os

source_path = "./input"
res_path = "./output"

class Personne:

    def __init__(self, nom, skills):
        self.nom = nom
        self.skills = skills


class Projet:

    def __init__(self,nom,duree,score,deadline,skills):
        self.nom = nom
        self.duree = duree
        self.score = score
        self.deadline = deadline
        self.skills = skills

class Skill:
    def __init__(self, nom):
        self.nom = nom

class Configuration:
    def __init__(self, projets):
        self.projets = [] 
        # [
        #     [projet , [personnes,....]]
        # ]

"""
TODO:
    return:
        [listePersonnes]
        [listeProjet]
        [listeSkills]
"""
def open_file(path):
    print("Ouverture de : {}".format(path))

    personnes = []
    projets = []
    
    with open(path, "r") as file:
        line = file.readline().split()

        nbContributeurs = int(line[0])
        nbProjets = int(line[1])

        #Pour chaque contributeurs
        for i in range(nbContributeurs):
            line = file.readline().split()
            p = Personne(line[0], [])
            personnes.append(p)

            #Pour chaque skill
            for j in range(int(line[1])):
                line = file.readline().split()
                p.skills.append([line[0], int(line[1])])

        #Pour chaque projets
        for k in range(nbProjets):
            line = file.readline().split()

            p = Projet(line[0],int(line[1]),int(line[2]),int(line[3]),[])
            projets.append(p)

            #Pour chaque skill
            for m in range(int(line[4])):
                line = file.readline().split()
                p.skills.append([line[0],int(line[1])])


    return personnes, projets

"""""
    return
        note
"""""
def noteConfig(config):

    note = 0
    jour = 0

    #TODO: Attention ne marche pas si des projets en parallèles
    for projet in config.projets:
        jour += projet[0].duree

        depassement = jour - projet[0].deadline

        if depassement < 0:
            depassement = 0

        note += projet[0].score - depassement

    return note

def realisable(personnes, projet):

    available = [personne for personne in personnes]

    nbSkillMatch = 0

    for skill in projet.skills:
        pasTrouve = True
        for personne in available:
            # Si la personne a dans ses skills le skill requis
            for skillPersonne in personne.skills:
                if skillPersonne[0] == skill[0]:
                    if skillPersonne[1] >= skill[1]:
                    #Si elle a une puissance suiffisante
                        available.remove(personne)
                        nbSkillMatch+=1
                        pasTrouve = False

        if pasTrouve:
            return False

    if(nbSkillMatch == len(projet.skills)):
        return True

    return False


"""
    return
        [NomDuProjet, [Personne1, Personne2,...]]
"""
def doProjet(personnes, projet):
    

    available = [personne for personne in personnes]

    personnesAssignees = []

    for skill in projet.skills:
        for personne in available:
            # Si la personne a dans ses skills le skill requis
            for skillPersonne in personne.skills:
                if skillPersonne[0] == skill[0]:
                    if skillPersonne[1] >= skill[1]:
                
                        personnesAssignees.append(personne.nom)
                        available.remove(personne)
                        if skillPersonne[1] == skill[1]:
                            skillPersonne[1]+= 1


    return [projet, personnesAssignees]

"""
    return
        config
"""
def generateConfig(personnes, projets):

    config = Configuration([])

    projetsAFaire = [projet for projet in projets]

    #FIXME: Impossible de sortir de la boucle si on peut faire un projet
    while len(projetsAFaire) > 0:

        projetsRealisables = [projet for projet in projetsAFaire if realisable(personnes, projet)]

        if len(projetsRealisables) == 0:
            break

        projet = projetsRealisables[0]

        #On le fait
        config.projets.append(doProjet(personnes, projet))
            
        projetsAFaire.remove(projet)

    return config

def save_file(file_path, config):
    with open(file_path, "w") as file:
        file.write(
            str(len(config.projets)) +
            "\n"
        )
        for projet in config.projets:
            file.write(
                projet[0].nom +
                "\n"
            )

            file.write(" ".join(projet[1]) + "\n")

if __name__ == "__main__":

    for file in sorted(os.listdir(source_path)):
        personnes, projets = open_file(os.path.join(source_path,file))

        config = generateConfig(personnes, projets)
        
        note = noteConfig(config)

        save_file(os.path.join(res_path,file), config)