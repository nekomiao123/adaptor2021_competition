import synapseclient 
import synapseutils 

syn = synapseclient.Synapse() 
syn.login('','') 

files = synapseutils.syncFromSynapse(syn, '', path='./trainingData/') 

