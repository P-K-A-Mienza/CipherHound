"""
CipherHound v_1, by Kojo Mienza
"""
from urllib.request import Request, urlopen
import re
import requests
import json

Req=''
WhaleAlertBulk=""
addholder=""
Balance_List=[]
BTCList=[]
WalletID_List=[]
riskList=[]
SanctionsRisk_List=[]
NonGambling_Risk_List=[]
WalletID_List=[]
Balance_List=[]
TotalSpendCount_List=[]
TotalSpent_List=[]
TotalDepositCount_List=[]
TotalDeposits_List=[]
OwnerData_List=[]
Subpoenable_List=[]
RiskSuperBulk=[]
RW_Add_List=[]
Cust_Raw_List=[]
exit=False


##API Check##
##Req= Request('https://api.whale-alert.io/v1/status?api_key=[yourAPIKey]', headers={'User-Agent':'Mozilla/5.0'})
##print (urlopen(Req).read().decode('utf-8'))

#Function for analyzing a custom list of addresses inserted via the UI
def custom(Cust_Adds):
    counter3=0
    while counter3<=len(Cust_Adds)-1:
        
        #Address Search query to CipherTrace
        url = " https://rest.ciphertrace.com/api/v1/address/search?features=ip&address="+Cust_Adds[counter3]+"&mempool=true" 
        payload={} 
        headers = { 'Authorization':'[yourapikey]'}
        response = requests.request("GET", url, headers=headers, data=payload) 
        AddressSearchBulk= json.loads(response.text)
       
        ##Get CipherTrace Risk and Sanctions Risk Scores
        url = "https://rest.ciphertrace.com/aml/v1/btc/risk?address="+Cust_Adds[counter3]
        payload={} 
        headers = { 'Authorization':'[yourApiKey]'}
        Riskresponse = requests.request("GET", url, headers=headers, data=payload) 
        riskbulk= json.loads(Riskresponse.text)
        
        print("\nAddress: " + str(AddressSearchBulk["address"]))
        print("General Risk Score:"+ str(riskbulk["risk"]))
        print("Sanctions Risk Score:"+ str(riskbulk["sanctionsRisk"]))
        print("Non Gambling Risk Score:" + str(riskbulk["gamblingOkRisk"]))
        print("Current Balance: " + str(AddressSearchBulk["currentBalance"]))
        print("Total Spend Count: " + str(AddressSearchBulk["totalSpendCount"]))
        print("Total Spent: "+ str(AddressSearchBulk["totalSpent"]))
        print("Total Deposit Count: "+ str(AddressSearchBulk["totalDepositCount"]))
        print("Total Deposits: "+ str(AddressSearchBulk["totalDeposits"]))
        print("Wallet Info:" + str(AddressSearchBulk["wallet"])+ "\n")
       
        #calculate and print risk score
        RWRiskScore=0
        RWRiskScore+=((riskbulk["sanctionsRisk"]+(riskbulk["gamblingOkRisk"]*1.5)+riskbulk["risk"])/3)
        matchObj = re.search('ransomware', Riskresponse.text)
        if matchObj:
            RWRiskScore+=9
            
        AggRisk=((riskbulk["gamblingOkRisk"]*1.5)+riskbulk["sanctionsRisk"]+riskbulk["risk"])/3
        RWRiskScore+=AggRisk
        
        if RWRiskScore>10:
            RWRiskScore=10
            
        print (" ' "+ str(AddressSearchBulk["address"])+"' - Ransomware Risk Score:"+ str(round(RWRiskScore,2))+"\n")

        if RWRiskScore>=7:
            print ("Address "+str(AddressSearchBulk["address"])+" is likely ransomware. Added to Likely Ransomware List.\n")
            RW_Add_List.append(str(AddressSearchBulk["address"]))
            
        counter3+=1
    
    
#Function for analyzing a stream of addresses from Whale Alert.io

def Whale_Alert(MinVal):
    Req= Request('https://api.whale-alert.io/v1/transactions?api_key=[yourApiKey]&min_value='+MinVal,
                 headers={'User-Agent':'Mozilla/5.0'})
    WhaleAlertBulk= (urlopen(Req).read().decode('utf-8'))
    ##WhaleAlertJson=json.loads(urlopen(Req).read().decode('utf-8'))
    
    
    #Place Addresses in List by address type
    TronList=re.findall ('"[a-zA-Z0-9]{34}"', WhaleAlertBulk) ##Add Tron Addresses to List
    ETHList=re.findall ('"[a-zA-Z0-9]{40}"', WhaleAlertBulk)  ##Add Ethereum Addresses to List
    BTCList=re.findall ('"[a-zA-Z0-9]{42}"', WhaleAlertBulk) ##Add 42 char BECH32 (P2WPKH) BTC Addresses to List
    BTCList+=re.findall ('"[a-zA-Z0-9]{62}"', WhaleAlertBulk) ## Add BeCh32 (P2WSH) BTC Addresses to list
    
    #Data cleansing/formatting
    BTCList= list(dict.fromkeys(BTCList)) ##Remove duplicates
    BTCList= [i.replace('"', '') for i in BTCList] ##remove quotes
    
    TronList= list(dict.fromkeys(TronList)) 
    TronList= [i.replace('"', '') for i in TronList] 
    
    ETHList= list(dict.fromkeys(ETHList))
    ETHList= [i.replace('"', '') for i in ETHList]
    
    counter=0

#Address Search query to CipherTrace
    while counter<=5 and len(BTCList)>0:
        
        url = " https://rest.ciphertrace.com/api/v1/address/search?features=ip&address="+BTCList[counter]+"&mempool=true" 
        payload={} 
        headers = { 'Authorization':'[yourApiKey]'}
        response = requests.request("GET", url, headers=headers, data=payload) 
        AddressSearchBulk= json.loads(response.text)
       
        ##Get CipherTrace Risk and Sanctions Risk Scores
        url = "https://rest.ciphertrace.com/aml/v1/btc/risk?address="+BTCList[counter]
        payload={} 
        headers = { 'Authorization':'[yourApiKey]'}
        Riskresponse = requests.request("GET", url, headers=headers, data=payload) 
        riskbulk= json.loads(Riskresponse.text)
      
        
        #print parsed data fields w/ labels
        print("Address: " + str(AddressSearchBulk["address"]))
        print("General Risk Score:"+ str(riskbulk["risk"]))
        print("Sanctions Risk Score:"+ str(riskbulk["sanctionsRisk"]))
        print("Non Gambling Risk Score:" + str(riskbulk["gamblingOkRisk"]))
        print("Current Balance: " + str(AddressSearchBulk["currentBalance"]))
        print("Total Spend Count: " + str(AddressSearchBulk["totalSpendCount"]))
        print("Total Spent: "+ str(AddressSearchBulk["totalSpent"]))
        print("Total Deposit Count: "+ str(AddressSearchBulk["totalDepositCount"]))
        print("Total Deposits: "+ str(AddressSearchBulk["totalDeposits"]))
        print("Wallet Info:" + str(AddressSearchBulk["wallet"])+ "\n")
        
        #calculate and print risk score
        RWRiskScore=0
        RWRiskScore+=((riskbulk["sanctionsRisk"]+(riskbulk["gamblingOkRisk"]*1.5)+riskbulk["risk"])/3)
        matchObj = re.search('ransomware', Riskresponse.text)
        if matchObj:
            RWRiskScore+=8
            
        AggRisk=((riskbulk["gamblingOkRisk"]*1.5)+riskbulk["sanctionsRisk"]+riskbulk["risk"])/3
        RWRiskScore+=AggRisk
        
        if RWRiskScore>10:
            RWRiskScore=10
        
        if RWRiskScore>=7:
            print ("Address "+str(AddressSearchBulk["address"])+" is likely ransomware. Added to Likely Ransomware List.")
            RW_Add_List.append(str(AddressSearchBulk["address"]))
            
        print (" ' "+ str(AddressSearchBulk["address"])+"' - Ransomware Risk Score:"+ str(round(RWRiskScore,2)))
        counter+=1
        
            
        
    
## Intro and getting user input
print ("Welcome to ChainHound.")
choice=input("Enter 1 if you would like to enter an address or list of addresses.\nEnter 2 if you would like to automatically check addresses captured by WhaleAlert.io. \n:")
MinVal=0

if choice=="1":
    counter2=0
    currchar=0
    Cust_Raw=input("Please enter one or more crypto addresses separated by a comma, with no spaces: ")
    while counter2<=len(Cust_Raw)-1 and exit !=True:
        currchar=ord(Cust_Raw[counter2])
        if ((currchar>=48 and currchar<=57) or (currchar>=65 and currchar<=90) or (currchar>=97 and currchar<=122)):
            addholder+=Cust_Raw[counter2]
        if counter2==len(Cust_Raw)-1 or currchar==44:
            Cust_Raw_List.append(addholder)
            addholder=""
        if counter2==len(Cust_Raw)-1 and currchar!=44:
            custom(Cust_Raw_List)
            exit=True
        counter2+=1
    
if choice=="2":
    MinVal=input("Enter the minimum transaction value you would like to be included in your trace (Value must be > 500000).")
    Whale_Alert(MinVal)

   
counter=0

#Print ransomware likely list  
i=0
print ("Ransomware Likely List:\n")
while i<=len(RW_Add_List)-1:
    print (RW_Add_List[i])
    i+=1
    


    

        

