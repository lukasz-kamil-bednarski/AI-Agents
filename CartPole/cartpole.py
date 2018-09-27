import gym
import random
import numpy as np
import tflearn
from statistics import median, mean

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical



env = gym.make("CartPole-v1")
env.reset()

def initial_population(initial_games = 10000, goal_steps = 500, score_requirement = 120):

    training_data = []
    scores = []
    accepted_scores = []
    labels = []
    for _ in range(initial_games):
        score = 0
        game_memory = []
       
        prev_observation = []

        for _ in range(goal_steps):
         
            action = random.randrange(0,2)

            observation, reward, done, info = env.step(action)
       
            if len(prev_observation) > 0 :
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score+=reward
            if done: break
        
        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:  
                training_data.append(data[0])
                labels.append(data[1])
        env.reset()
    
        scores.append(score)
    
    training_data_save = np.array(training_data)
    #np.save('cartpole-v0.npy',training_data_save)
    
    print('Average accepted score:',mean(accepted_scores))
    
    return np.array(training_data), labels

    

train_data, labels = initial_population()

labels = to_categorical(labels, 2)

model = Sequential()
model.add(Dense(units = 128, input_dim = 4))
model.add(Dense(units = 256, activation = 'relu'))
model.add(Dense(units = 512, activation = 'relu'))
model.add(Dense(units = 256, activation = 'relu'))
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dense(units = 2, activation = 'softmax'))
    
model.compile(loss='categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

model.fit(train_data, labels, epochs = 10)

#model.save("cartpole_model.h5")


###
scores = []
choices = []

for each_game in range(10):
    score = 0
    game_memory = []
    prev_obs = []
    env.reset()
    
    for t in range(10000):
        env.render()
        
        if len(prev_obs) == 0:
            action = random.randrange(0, 2)
        else:
            action = np.argmax(model.predict(np.array([prev_obs])))
        choices.append(action)
        
        new_obs , reward, done, info = env.step(action)
        
        prev_obs = new_obs
        
        game_memory.append([new_obs, action])
        
        score += reward
        
        if done:
            break
    scores.append(score)
print("Avg:", mean(scores))




