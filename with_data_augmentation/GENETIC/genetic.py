import random
import statistics
import pandas as pd
INF = float('inf')


class Genetic(object):

    def __init__(self,num_ind_by_generation,num_Gen,mutation_probability)->None:
        self.nIndGen = num_ind_by_generation
        self.nGen = num_Gen
        self.pMut = mutation_probability
        
    def run(self)->list:
        generacion = self.primeraGen(self.nIndGen)
        while self.nGen > 0:
            generacion = self.sortGeneration(generacion)
            #print(generacion[0])
            generacion = self.descarte(generacion)
            children = list()
            while len(children) + len(generacion) < self.nIndGen:
                parent1, parent2 = self.seleccion(generacion)
                child1, child2 = self.cruce(parent1,parent2)
                child1 = self.mutacion(child1, self.pMut)
                child2 = self.mutacion(child2, self.pMut)
                children.append(child1)
                children.append(child2)
            generacion = generacion + children
            self.nGen = self.nGen - 1
        
        #print(generacion)
        return generacion

    def seleccion(self,generacion)->tuple:
        tGen = len(generacion)
        ind1 = random.randint(0, tGen-1)
        ind2 = ind1
        while ind1 == ind2:
            ind2 = random.randint(0,tGen-1)
        return generacion[ind1], generacion[ind2]

    def descarte(self,generacion)->list:
        tGen = len(generacion)
        return generacion[:tGen>>1] # podar mas 

    def cruce(self,ind1,ind2)->tuple:
        tInd = len(ind1)
        pivot = random.randint(0,tInd-1)
        new1 = ind1[:pivot] + ind2[pivot:]
        new2 = ind2[:pivot] + ind1[pivot:] 
        return new1, new2

    def mutacion(self,ind, prob)->list:
        global density
        p = random.randint(1,100)
        if p < prob*100: 
            tInd = len(ind)
            q = random.randint(0,tInd-1)
            min_val,max_val,_,_ = density[q]
            ind[q] = random.uniform(min_val,max_val)
        return ind


    def newInd(self)->list:
        global density
        ind = list()
        for i in range(len(density)):
            min_val,max_val,_,_ = density[i]
            ind.append(random.uniform(min_val,max_val))
        return ind

    def primeraGen(self,nIndGen)->list:
        generacion = list()
        while len(generacion) < nIndGen:
            generacion.append(self.newInd())
        return generacion

    def fitness(self,ind)->float:
        global density
        
        score = 0
        n = len(ind)
        for i in range(n):
            min_val,max_val,avg,std = density[i]
            
            ind_val_i = ind[i]
            if  ind_val_i>= min_val and ind_val_i <= max_val:
                score +=5

                if ind_val_i >= avg - std and ind_val_i <= avg + std:
                    score += 10
        return score


    def sortGeneration(self,generacion)->list:
        weighted = list()
        for ind in generacion:
            score = self.fitness(ind)
            weighted.append((ind,score))
        
        weighted.sort(key = lambda x: -x[1])
        
        ordered = list()
        
        for (x,y) in weighted:
            ordered.append(x)
        return ordered    

# funciones auxiliares
def load_dataset(file_name,target)->tuple:
    df = pd.read_excel(file_name)
    df = df[df["cure_or_fail"] == target]
    #print(df)
    df.drop('cure_or_fail', inplace=True, axis=1)
    df_list = df.values.tolist()
    return list(df.columns),df_list

def calculate_density(names,df)->list:
    ans = list()
    visible = dict()
    n_rows = len(df)
    n_cols = len(df[0])
    for j in range(n_cols):
        min_val = INF
        max_val = - INF
        suma = 0
        col = list() 
        for i in range(n_rows):
            min_val = min(min_val,df[i][j])
            max_val = max(max_val,df[i][j])
            suma += df[i][j]
            col.append(df[i][j]) 
        
        prom = suma/n_rows
        stdv =  statistics.stdev(col)


        tmp = [min_val,max_val,prom,stdv]
        ans.append(tmp)
        visible[names[j]] = tmp


    #print(visible)
    return ans

def filter_gen(best_gen)->list:
    global density
    score = 0
    verified = list()
    for ind in best_gen:
        band = True
        for i in range(len(ind)):
            min_val,max_val,avg,std = density[i]
            
            ind_val_i = ind[i]
            if  ind_val_i>= min_val and ind_val_i <= max_val:
                score +=5

                if ind_val_i >= avg - std and ind_val_i <= avg + std:
                    score += 10

                else:
                    band = False
            else:
                band = False
        if band:
            verified.append(ind)
    
    return verified

def write_csv(gen, names, target)->None:
    for ind in gen:
        ind.append(target)

    names.append("cure_or_fail")
    df = pd.DataFrame(gen, columns = names )
    df.to_excel("genetic_augmented_target={}.xlsx".format(target), index = False)

def merge():
    fail = "genetic_augmented_target=1.xlsx"
    fail = pd.read_excel(fail)



    cure = "genetic_augmented_target=0.xlsx"
    cure = pd.read_excel(cure)

    df = fail.append(cure)
    df.to_excel("genetic_augmented_target=01.xlsx",index = False)    
    
def main()->None:
    global density

    # target  = 0

    file_name = "../../without_data_augmentation/preprocesado.xlsx"
    target = 0
    names,df_list = load_dataset(file_name, target)
    density = calculate_density(names,df_list)

    ind_x_gen = 5000
    nro_gen = 100
    prob_mut = 0.05
    g = Genetic(ind_x_gen,nro_gen, prob_mut)
    best_gen = g.run()
    filtered_gen = filter_gen(best_gen)[:200]
    write_csv(filtered_gen, names, target)

    # target  = 1

    file_name = "../../without_data_augmentation/preprocesado.xlsx"
    target = 1
    names,df_list = load_dataset(file_name, target)
    density = calculate_density(names,df_list)

    ind_x_gen = 5000
    nro_gen = 100
    prob_mut = 0.05
    g = Genetic(ind_x_gen,nro_gen, prob_mut)
    best_gen = g.run()
    filtered_gen = filter_gen(best_gen)[:200]
    write_csv(filtered_gen, names, target)

main()
