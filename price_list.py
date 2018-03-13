
# -*- coding: utf8 -*-


import requests
import json
import boto3
import getopt, sys

pricing_url='https://pricing.us-east-1.amazonaws.com'

reg2loc = {'us-east-1': 'US East (N. Virginia)',
  'us-east-2':'US East (Ohio)',
  'us-west-1':'US West (N. California)',
  'us-west-2':'US West (Oregon)',
  'ca-central-1':'Canada (Central)',
  'eu-central-1':'EU (Frankfurt)',
  'eu-west-1':'EU (Ireland)',
  'eu-west-2':'EU (London)',
  'eu-west-3':'EU (Paris)',
  'ap-northeast-1':'Asia Pacific (Tokyo)',
  'ap-northeast-2':'Asia Pacific (Seoul)',
  'ap-northeast-3':'Asia Pacific (Osaka-Local)',
  'ap-southeast-1':'Asia Pacific (Singapore)',
  'ap-southeast-2':'Asia Pacific (Sydney)',
  'ap-south-1':'Asia Pacific (Mumbai)',
  'sa-east-1':'South America (São Paulo)'}

loc2reg = {v: k for k, v in reg2loc.iteritems()}

mode='normal'
# mode='raw'

def usage ():
  print ('Usage:')
  print (' price_list.py [OPTION]... [REGION]')
  print ('')
  print (' REGION  Region to ask, if omits then use the default region')
  print ('')
  print ('Options:')
  print ('-h, --help		 This help')
  print ('-r, --list_regions     List regions available')
  print ('-s, --list_services    List services available')
  print ('-o SERVICE, --list_offer=SERVICE       List offer available for a region')

def main ():
  
  try:
    options, remainder = getopt.getopt(sys.argv[1:], 'hrso:')
  except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

  if len(remainder) == 1:
    region = remainder.pop()

  for opt,arg in options:
    if opt in ('-h','--help'):
      usage()
      print reg2loc
      print loc2reg
      sys.exit(0)

    elif opt in ('-r','--list_regions'):
#      ec2=boto3.client('ec2')
#      regions = ec2.describe_regions()

#   -- Salvar a disco las regiones: ahorrar llamadas a la API      
#      with open('../regions.txt','w') as outfile:
#       json.dump(regions,outfile)
#   -- Leer de disco las regiones: ahorrar llamadas a la API      
      with open('../regions.txt','r') as infile:
        regions = json.load(infile)
#   -- FIN ahorro llamadas api

      if mode == 'raw':
        print json.dumps(regions,indent=4, sort_keys=True)
      else:
        for reg in regions["Regions"]:
          print reg['RegionName']

    elif opt in ('-s','--list_services'):
      r = requests.get(pricing_url+'/offers/v1.0/aws/index.json')
      if mode == 'raw':
        print json.dumps(r.json(),indent=4, sort_keys=True)
      else:
        for srv in r.json()["offers"]:
          print srv

    elif opt in ('-o','--list_offer'):
      r = requests.get(pricing_url+'/offers/v1.0/aws/index.json')
      ep_oferta=r.json()["offers"][arg]["currentVersionUrl"]
      print pricing_url+ep_oferta
      print
      r = requests.get(pricing_url+ep_oferta,stream=True)
      for line in r.iter_lines():
        print line
#      print json.dumps(r.json(),indent=4, sort_keys=True)



if __name__ == "__main__":
    main()      
