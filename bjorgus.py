from discord.ext import commands
import discord
from discord.ui import Button, View, Select
import json
import random
class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    table_hazard = [3,2,7,9,6,2,8,2,5,6,
                    4,1,3,8,7,1,6,8,4,0,
                    2,5,0,4,8,6,6,8,4,1,
                    0,5,9,5,7,0,9,4,6,5,
                    2,8,2,5,6,3,2,7,9,6,
                    1,6,8,4,0,4,1,3,8,7,
                    7,5,6,2,0,4,1,6,3,1,
                    6,6,8,4,1,2,5,0,4,8,
                    0,9,1,6,5,0,5,9,5,7]
    table_coups_portés= [[[-6,0],[-7,0],[-8,0],[-9,0],[-10,0],[-11,0],[-12,0],[-14,0],[-16,0],[-18,0],[-999,0],[-999,0],[-999,0]],
                         [[-0,-999],[-0,-999],[-0,-8],[-0,-6],[-1,-6],[-2,-5],[-3,-5],[-4,-5],[-5,-4],[-6,-4],[-7,-4],[-8,-3],[-9,-3]],
                         [[-0,-999],[-0,-8],[-0,-7],[-1,-6],[-2,-5],[-3,-5],[-4,-4],[-5,-4],[-6,-3],[-7,-3],[-8,-3],[-9,-3],[-10,-2]],
                         [[-0,-8],[-0,-7],[-1,-6],[-2,-5],[-3,-5],[-4,-4],[-5,-4],[-6,-3],[-7,-3],[-8,-3],[-9,-2],[-10,-2],[-11,-2]],
                         [[-0,-8],[-1,-7],[-2,-6],[-3,-5],[-4,-4],[-5,-4],[-6,-3],[-7,-3],[-8,-2],[-9,-2],[-10,-2],[-11,-2],[-12,-2]],
                         [[-1,-7],[-2,-6],[-3,-5],[-4,-4],[-5,-4],[-6,-3],[-7,-2],[-8,-2],[-9,-2],[-10,-2],[-11,-2],[-12,-2],[-14,-1]],
                         [[-2,-6],[-3,-6],[-4,-5],[-5,-4],[-6,-3],[-7,-2],[-8,-2],[-9,-2],[-10,-2],[-11,-1],[-12,-1],[-14,-1],[-16,-1]],
                         [[-3,-5],[-4,-5],[-5,-4],[-6,-3],[-7,-3],[-8,-2],[-9,-1],[-10,-1],[-11,-1],[-12,-0],[-14,-0],[-16,-0],[-18,-0]],
                         [[-4,-4],[-5,-4],[-6,-3],[-7,-2],[-8,-1],[-9,-1],[-10,-0],[-11,-0],[-12,0],[-14,0],[-16,0],[-18,0],[-999, 0]],
                         [[-5,-3],[-6,-3],[-7,-2],[-8,0],[-9,0],[-10,0],[-11,0],[-12,0],[-14,0],[-16,0],[-18,0],[-999,0],[-999,0]]]
    @commands.command(name="start") #Décorateur qui indique que la fonction suivante sera une fonction de commande
    async def start(self, ctx): #Fonction qui crée une fiche de personnage pour l'utilisateur qui lance la commande
        fiche_perso = {  #Créé la fiche de personnage
            "Habilete" : random.choice(self.table_hazard)+10,
            "Volonte" : random.choice(self.table_hazard)+20,
            "Endurance" : random.choice(self.table_hazard)+20, 
            "Magies mineures" : [],
            "Inventaire" : {},
            "paragraphe" : 1,
            "armes" : ["poings", "baguette"],
        }
        with open("users.json", "r", encoding="utf8") as users: 
            userdic = json.load(users)
            userdic[str(ctx.author.id)] = fiche_perso
        with open("users.json", "w", encoding="utf8") as users: #Ajoute la fiche de personnage a la liste des fiches de personnage
            json.dump(userdic, users)         
        await ctx.send(f"```Bienvenue! Avant de commencer votre aventure, vous devez creer un personnage. Ses statistiques ont déjà été choisies aléatoirement et sont : \nHabileté au combat : {fiche_perso['Habilete']}\nVolonté : {fiche_perso['Volonte']}\nEndurance : {fiche_perso['Endurance']}```")
        await self.select_spells(ctx) #indique au module que la fonction suivante sera une fonction de commande
    #Fonction qui vérifie que l'utilisateur qui a cliqué sur un bouton est bien celui qui a lancé la commande
    async def select_spells(self, ctx): #Fonction qui demande au joueur de choisir ses sorts
        rotanumber = 0
        load_sorts = open("sorts.json", "r", encoding="utf8")
        sorts = json.load(load_sorts)
        # Définition de l'embed du message
        name = [f"{i+1}. {list(sorts)[i]}" for i in range(len(sorts))]
        value = [sorts[list(sorts)[i]] for i in range(len(sorts))]
        embed_choix_sorts  = discord.Embed(title = "Choix des magies mineures", description ="Choisissez vos s magies mineures parmi la liste ci dessous", colour = 0xFFFF00)
        embed_choix_sorts.add_field(name = name[rotanumber], value = value[rotanumber])

        #Définition des boutons liés au message
        droite = Button(emoji="➡️", style = discord.ButtonStyle.gray)
        gauche = Button(emoji="⬅️", style = discord.ButtonStyle.gray)
        Select_Spells = Select(
            
            options = [discord.SelectOption(label = element) for element in sorts],
            min_values=5,
            max_values=5
        )

        view = View() #Créé la variable view nécessaire a discord pour afficher des objet interactifs
        #ajoute les bouttons au View
        view.add_item(gauche)
        view.add_item(droite)
        view.add_item(Select_Spells)
        #Créations des fonctions liées aux bouttons
        async def select_spells_callback(interaction):
            nonlocal ctx
            if self.usercheck(interaction, ctx):
                #Ajout des sorts choisis par le joueur a sa fiche
                with open("users.json", "r+", encoding="utf8") as users:
                    userdic = json.load(users)
                    userdic[str(ctx.author.id)]["Magies mineures"] = Select_Spells.values
                with open("users.json", "w", encoding="utf8") as users:    
                    json.dump(userdic, users)
                #Envoie d'un message de confirmation
                await interaction.response.send_message("```Vous avez choisi les sorts suivants : " + self.listtostring(Select_Spells.values)+"```")
                await self.select_inventory(ctx)        
            else:
                #Envoie d'un message d'erreur si le joueur n'est pas celui qui a lancé la commande
                await interaction.response.send_message("hey, il ne s'agit pas de ta fiche! Si tu veux t'en créer une et commencer ton aventure, utilise la commande $start.", ephemeral = True)
        async def droite_callback(interaction): #Fonction qui fait défiler les sorts vers la droite
            if self.usercheck(interaction, ctx):
                nonlocal rotanumber
                try:
                    name[rotanumber+1]
                    rotanumber += 1
                except:
                    rotanumber = 0
                embed_choix_sorts = discord.Embed(title = "Choix des magies mineures", description ="Choisissez vos s magies mineures parmi la liste ci dessous", colour = 0xFFFF00)
                embed_choix_sorts.add_field(name = name[rotanumber], value = value[rotanumber]) 
                await interaction.response.edit_message(embed = embed_choix_sorts, view = view)
            else:
                await interaction.response.send_message("hey, il ne s'agit pas de ta fiche! Si tu veux t'en créer une et commencer ton aventure, utilise la commande $start.", ephemeral = True)
        async def gauche_callback(interaction): #Fonction qui fait défiler les sorts vers la gauche
            if self.usercheck(interaction, ctx):
                nonlocal rotanumber
                try :
                    name[rotanumber-1]
                    rotanumber -= 1
                except :
                    rotanumber = len(name)-1
                embed_choix_sorts = discord.Embed(title = "Choix des magies mineures", description ="Choisissez vos s magies mineures parmi la liste ci dessous", colour = 0xFFFF00)
                embed_choix_sorts.add_field(name = name[rotanumber], value = value[rotanumber])
                await interaction.response.edit_message(embed = embed_choix_sorts, view = view)
            else:
                await interaction.response.send_message("hey, il ne s'agit pas de ta fiche! Si tu veux t'en créer une et commencer ton aventure, utilise la commande $start.", ephemeral = True)


        #Assignation des fonctions a leurs boutons respectifs
        Select_Spells.callback = select_spells_callback
        droite.callback = droite_callback
        gauche.callback = gauche_callback

        #Envoie du message
        await ctx.send(embed = embed_choix_sorts, view = view)
    async def select_inventory(self, ctx): #Fonction qui fait faire au joueur plusieurs choix concernant son inventaire.
        load_inventaire = open("Inventaire.json", "r", encoding="utf8")
        inventaire = json.load(load_inventaire)        
        embed_inventaire = discord.Embed(title = "Inventaire", description = inventaire["paragraphe"], color=0xFFFF00)
        select_inventaire = Select( #Créé le menu déroulant
            options = [discord.SelectOption(label=element) for element in inventaire["inventaire choix"]]
        )
        view = View() #Créé la variable view qui stoque les objets interactifs
        view.add_item(select_inventaire) #Ajoute le menu déroulant à la variable view
        async def Select_inv_callback(interaction): #Fonction qui gère les changements de paragraphe
            nonlocal inventaire
            with open("users.json", "r", encoding="utf8") as users:
                fiche_perso = json.load(users)

                fiche_perso[str(ctx.author.id)]["Inventaire"] = inventaire["inventaire fixe"]
                fiche_perso[str(ctx.author.id)]["Inventaire"][self.listtostring(select_inventaire.values)] = 1
                for a in inventaire["armes"]:
                    if a in fiche_perso[str(ctx.author.id)]["Inventaire"]:
                        fiche_perso[str(ctx.author.id)]["armes"].append(a)
            with open("users.json", "w", encoding="utf8") as users:
                json.dump(fiche_perso, users)
            await interaction.response.send_message("```Vous avez choisi " + self.listtostring(select_inventaire.values)+"```")
            await self.embed_info(ctx)
        select_inventaire.callback = Select_inv_callback
        await ctx.send(embed = embed_inventaire, view = view)
    #Fonction qui affiche les informations nécéssaires avant le début du jeu.
    async def embed_info(self, ctx): #Fonction qui affiche les informations nécéssaires avant le début du jeu.
        embed_ecoulees = 0
        with open("Informations.json", "r", encoding='utf-8') as f:
            informations = json.load(f)
        view = View() #Créé la variable view qui stoque les objets interactifs
        Button_validation = Button(emoji="✅", style = discord.ButtonStyle.green)
        view.add_item(Button_validation)
        async def Button_validation_callback(interaction): #Fonction qui gère les changements de paragraphes
            nonlocal embed_ecoulees
            if self.usercheck(interaction, ctx):
                if embed_ecoulees < len(informations)-1:
                    embed_ecoulees += 1
                    await interaction.response.edit_message(embed = discord.Embed(title = informations[embed_ecoulees][0], description=informations[embed_ecoulees][1]), view = view)
                else:
                    await self.resume(ctx)
            else:
                await interaction.response.send_message("hey, il ne s'agit pas de ta fiche! Si tu veux t'en créer une et commencer ton aventure, utilise la commande $start.", ephemeral = True)
        Button_validation.callback = Button_validation_callback
        await ctx.send(embed = discord.Embed(title = informations[embed_ecoulees][0], description=informations[embed_ecoulees][1]), view = view)

    @commands.command(name="resume")
    async def resume(self, ctx): #Fonction qui permet de reprendre la partie là où on l'avait laissée
        with open("users.json", "r", encoding="utf8") as users:
            fiche_perso = json.load(users)
            nbr_paragraphe = fiche_perso[str(ctx.author.id)]["paragraphe"]
        await self.rota_paragraphes(ctx, nbr_paragraphe)


    async def rota_paragraphes(self, ctx, nombre): #Fonction qui fait défiler les paragraphes
        with open("users.json", "r", encoding="utf8") as p: #Récupère le paragraphe actuel du joueur
            fiche_perso = json.load(p)
            fiche_perso[str(ctx.author.id)]["paragraphe"] = nombre #Sauvegarde le paragraphe dans le fichier users.json
        with open("users.json", "w", encoding="utf8") as p:
            json.dump(fiche_perso, p)
        with open("paragraphe.json", "r", encoding="utf8") as p: #Récupère les paragraphes
            paragraphes = json.load(p)
        async def one_callback(interaction): 
            await bouttons_callback(1, interaction)
        async def two_callback(interaction):
            await bouttons_callback(2, interaction)
        async def three_callback(interaction):
            await bouttons_callback(3, interaction)
        async def four_callback(interaction):
            await bouttons_callback(4, interaction)
        async def five_callback(interaction):
            await bouttons_callback(5, interaction)
        async def six_callback(interaction):
            await bouttons_callback(6, interaction)
        async def seven_callback(interaction):
            await bouttons_callback(7, interaction)
        async def eight_callback(interaction):
            await bouttons_callback(8, interaction)
        async def nine_callback(interaction):
            await bouttons_callback(9, interaction)
        async def ten_callback(interaction):
            await bouttons_callback(10, interaction) #Fonctions qui gèrent les boutons
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣","5️⃣", "6️⃣", "7️⃣", "8️⃣","9️⃣", "🔟"]
        buttons = [Button(emoji=emojis[i], style = discord.ButtonStyle.gray) for i in range(len(paragraphes[str(nombre)]["choix"]))]
        callbacks = [one_callback, two_callback, three_callback, four_callback, five_callback, six_callback, seven_callback, eight_callback, nine_callback, ten_callback]

        for k in range(len(paragraphes[str(nombre)]["choix"])): #Ajoute les fonctions aux boutons
            buttons[k].callback = callbacks[k]
        async def bouttons_callback(numero,interaction): #Fonction qui gère les changements de paragraphes
            nonlocal ctx
            nonlocal buttons
            nonlocal nombre
            nonlocal paragraphes
            nombre_suivant = paragraphes[str(nombre)]["choix"][numero-1] #Définit le numero du paragraphe suivant
            if self.usercheck(interaction, ctx):
                if paragraphes[str(nombre_suivant)]["combat"]: #Si le paragraphe suivant est un combat
                    await interaction.response.edit_message(embed = await self.embed_paragraphe(nombre_suivant)) #Envoie le paragraphe suivant
                    await self.choix_arme(ctx, paragraphes[str(nombre_suivant)]["adversaires"], paragraphes[str(nombre_suivant)]) #Demande au joueur de choisir son arme, puis lance le combat
                else:
                    view = View()
                    for k in range(len(paragraphes[str(nombre)]["choix"])): #Ajoute les fonctions aux boutons
                        view.add_item(buttons[k])
                        buttons[k].callback = callbacks[k]
                    with open("users.json", "r", encoding="utf8") as p: 
                        fiche_perso = json.load(p)
                    with open("users.json", "w", encoding="utf8") as p: #Sauvegarde le paragraphe dans le fichier users.json
                        fiche_perso[str(ctx.author.id)]["paragraphe"] = nombre_suivant
                        json.dump(fiche_perso, p)
                    nombre = nombre_suivant
                    await interaction.response.edit_message(embed = await self.embed_paragraphe(nombre_suivant), view = view) #Envoie le paragraphe suivant
        view = View() #Créé la variable view qui stoque les objets interactifs
        for k in range(len(paragraphes[str(nombre)]["choix"])):
            view.add_item(buttons[k])
            buttons[k].callback = callbacks[k]
        await ctx.send(embed = await self.embed_paragraphe(nombre), view = view)

    async def embed_paragraphe(self,nombre): #Fonction qui crée un embed avec le paragraphe demandé
        with open("paragraphe.json", "r", encoding = "utf8") as f:
            textes = json.load(f)[str(nombre)]["content"]
        return discord.Embed(title = textes[0], description= textes[1])
    

    async def choix_arme(self, ctx, adversaires, paragraphe): #Fonction qui demande au joueur de choisir son arme
        with open('users.json', 'r', encoding='utf8') as f:
            user = json.load(f)
        select = Select(options=[discord.SelectOption(label=element) for element in user[str(ctx.author.id)]["armes"]], placeholder="Choisissez votre arme")
        view = View() #Créé la variable view qui stoque les objets interactifs
        view.add_item(select) #Ajoute le menu déroulant à la variable view
        async def select_callback(interaction):
            await self.combat(ctx, adversaires, select.values[0], paragraphe) #Lance la fonction combat avec l'arme choisie
        select.callback = select_callback
        await ctx.send("Vous êtes engagé dans un combat!", view = view)

    async def combat(self, ctx, adversaires : list, arme, paragraphe): #Fonction qui gère le combat
        with open("users.json", "r", encoding = "utf8") as f:
            user = json.load(f)
        habileté = user[str(ctx.author.id)]["Habilete"]
        if arme != "poings" and arme != "baguette":
            habileté -= 6
        elif arme == "poings":
            habileté -= 8
        #Applique les regles d'habileté en fonction de l'arme utilisée
        embed = discord.Embed(title = "Combat!", description = "Vous êtes engagé dans un combat!")
        for k in adversaires:
            embed.add_field(name = k[0], value = f"Endurance : {k[1]}\nHabileté : {k[2]}")
        async def selection_volonte_callback(interaction): #Fonction qui gère le combat si le joueur utilise une baguette
            nonlocal adversaires
            nonlocal ctx
            nonlocal select
            nonlocal user
            nonlocal self #Permet d'utiliser les variables de la fonction mère dans la fonction
            if self.usercheck(interaction, ctx): #Vérifie que l'utilisateur qui a cliqué sur le bouton est bien celui qui a lancé la commande
                longueur_adversaires = len(adversaires)
                for k in range(len(adversaires)): #Pour chaque adversaire
                    nombre_morts = longueur_adversaires - len(adversaires) #On calcule le nombre d'adversaires morts pour ne pas avoir d'erreur d'index
                    resultat = await self.table_combat(adversaires[k- nombre_morts], habileté)
                    user[str(ctx.author.id)]["Endurance"] += resultat[1] #On ajoute la perte d'endurance à l'endurance du joueur
                    adversaires[k-nombre_morts][1] += resultat[0]*int(select.values[0]) #On multiplie le résultat du combat par le nombre de points de volonté dépensés
                    if adversaires[k-nombre_morts][1] <= 0:
                        adversaires.pop(k-nombre_morts) #Si un adversaire est mort, on le supprime de la liste des adversaires
                    if len(adversaires) == 0: #Si tous les adversaires sont morts, arrete le combat
                        break
                
                view = View() #Créé la variable view qui stoque les objets interactifs
                view.add_item(select) #Ajoute le menu déroulant à la variable view
                select.callback = selection_volonte_callback #Assignation de la fonction selection_volonte_callback au menu
                embed = discord.Embed(title = "Combat!", description = "Vous êtes engagé dans un combat!") #Créé un embed qui contiendra les informations du combat
                for k in range(len(adversaires)):
                    embed.add_field(name = adversaires[k][0], value = f"Endurance : {adversaires[k][1]}\nHabileté : {adversaires[k][2]}") #Ajoute les adversaires au message
                await interaction.response.edit_message(embed = embed, view = view) #Envoie un message avec les nouveaux points d'endurance des adversaires
                if user[str(ctx.author.id)]["Endurance"] <= 0:
                    user.pop(str(ctx.author.id)) #Si le joueur est mort, on supprime sa fiche de personnage
                    await ctx.send("Vous etes mort")
                elif len(adversaires) == 0: #Si le joueur a gagné le combat
                    await ctx.send("Vous avez gagné le combat!")
                    await self.rota_paragraphes(ctx, paragraphe["choix"][0]) #Envoie au paragraphe suivant
                    return
                with open("users.json", "w", encoding = "utf8") as f:  #Sauvegarde les changements dans le fichier users.json
                    json.dump(user, f)
            else:
                await interaction.response.send_message("hey, il ne s'agit pas de ton combat, patouch!", ephemeral = True) #Envoie d'un message d'erreur si le joueur n'est pas celui qui a lancé la commande

        if arme == "baguette": #Créé un menu déroulant demandant le nombre de points de volonté que le joueur veut dépenser et l'envoie
            options = [discord.SelectOption(label = str(i+1)) for i in range(user[str(ctx.author.id)]["Volonte"])]
            if len(options) > 25: #Si le joueur a plus de 25 points de volonté, le menu déroulant ne peut pas contenir plus de 25 options donc on le limite à 25 options
                options = options[:24]
            select = Select( #Créé le menu déroulant
                placeholder="nombre de points de VOLONTE à dépenser",
                options = options
            )
            view = View() #Créé la variable view qui stoque les objets interactifs
            view.add_item(select)
            select.callback = selection_volonte_callback #Assignation de la fonction selection_volonte_callback au menu
            await ctx.send(embed = embed, view = view) #Envoie le menu déroulant
        else: #Si le joueur n'utilise pas de baguette, il n'a pas besoin de dépenser de points de volonté
            for k in range(len(adversaires)):
                resultat = await self.table_combat(adversaires[k], habileté)
                user[str(ctx.author.id)]["Endurance"] += resultat[1]
                adversaires[k][1] += resultat[0]
                if adversaires[k][1] <= 0:
                    adversaires.pop(k)
                if len(adversaires) == 0:
                    await ctx.send("Vous avez gagné le combat!")
                    await self.rota_paragraphes(ctx, paragraphe["choix"][0])
                    return
                if user[str(ctx.author.id)]["Endurance"] <= 0:
                    await ctx.send("Vous etes mort")
                    user.pop(str(ctx.author.id))
                    return
            with open("users.json", "w", encoding = "utf8") as f:  
                json.dump(user, f)
            await self.combat(ctx, adversaires, arme, paragraphe)
        with open("users.json", "w", encoding = "utf8") as f:  #Sauvegarde les changements dans le fichier users.json
            json.dump(user, f)
    async def table_combat(self, adversaire, habileté): #Fonction qui détermine le résultat d'un tour de combat
            quotient_attaque = habileté - adversaire[2]
            if quotient_attaque <= -11:
                return  self.table_coups_portés[random.choice(self.table_hazard)][0][0],self.table_coups_portés[random.choice(self.table_hazard)][0][1]
            elif quotient_attaque <= -9:
                return  self.table_coups_portés[random.choice(self.table_hazard)][1][0],self.table_coups_portés[random.choice(self.table_hazard)][1][1]
            elif quotient_attaque <= -7:
                return  self.table_coups_portés[random.choice(self.table_hazard)][2][0],self.table_coups_portés[random.choice(self.table_hazard)][2][1]
            elif quotient_attaque <=-5:
                return  self.table_coups_portés[random.choice(self.table_hazard)][3][0],self.table_coups_portés[random.choice(self.table_hazard)][3][1]
            elif quotient_attaque <= -3:
                return  self.table_coups_portés[random.choice(self.table_hazard)][4][0],self.table_coups_portés[random.choice(self.table_hazard)][4][1]
            elif quotient_attaque <= -1:
                return  self.table_coups_portés[random.choice(self.table_hazard)][5][0],self.table_coups_portés[random.choice(self.table_hazard)][5][1]
            elif quotient_attaque == 0:
                return  self.table_coups_portés[random.choice(self.table_hazard)][6][0],self.table_coups_portés[random.choice(self.table_hazard)][6][1]
            elif quotient_attaque <= 2:
                return  self.table_coups_portés[random.choice(self.table_hazard)][7][0],self.table_coups_portés[random.choice(self.table_hazard)][7][1]
            elif quotient_attaque <= 4:
                return  self.table_coups_portés[random.choice(self.table_hazard)][8][0],self.table_coups_portés[random.choice(self.table_hazard)][8][1]
            elif quotient_attaque <= 6:
                return  self.table_coups_portés[random.choice(self.table_hazard)][9][0],self.table_coups_portés[random.choice(self.table_hazard)][9][1]   
            elif quotient_attaque <= 8:
                return  self.table_coups_portés[random.choice(self.table_hazard)][10][0],self.table_coups_portés[random.choice(self.table_hazard)][10][1]
            elif quotient_attaque <= 10:
                return  self.table_coups_portés[random.choice(self.table_hazard)][11][0],self.table_coups_portés[random.choice(self.table_hazard)][11][1]
            elif quotient_attaque >= 11:
                return  self.table_coups_portés[random.choice(self.table_hazard)][12][0], self.table_coups_portés[random.choice(self.table_hazard)][12][1]
    def usercheck(self, interaction, ctx): #Fonction qui vérifie que l'utilisateur qui a cliqué sur un bouton est bien celui qui a lancé la commande
        return interaction.user == ctx.author
    #Fonction qui transforme une liste en string sans les crochets et les apostrophes
    def listtostring(self, liste):
        string = str(liste)
        string = string.replace("'", "")
        string = string.replace("[", "")
        string = string.replace("]", "")
        return string
async def setup(bot):
    await bot.add_cog(Cogs(bot))