#!python
# -*- coding: utf-8 -*-

import json
import requests

webServiceAddress = 'http://localhost:3001'

class restfulBookerConnection():
    def __init__(self):
        self.webServiceAddress = 'http://localhost:3001'

    def pingWebService(self):
        resp = requests.get(webServiceAddress)
        print resp.status_code
        return resp.status_code

    def getBookings(self,arguments=''):
        url=webServiceAddress + '/booking'+arguments
        resp = requests.get(url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise Exception('GET /booking/ {}'.format(resp.status_code))
        print str(resp.json())
        return resp.json()

    def getBookingsIds(self,arguments=''):
        id_list=[]
        url=webServiceAddress + '/booking'+arguments
        resp = requests.get(url)
        if resp.status_code != 200: # This means something went wrong.
            raise Exception('GET /booking/ {}'.format(resp.status_code))
        print str(resp.json())
        for item in resp.json():
            id_list.append(item['bookingid'])
        return sorted(id_list)

    def getLastBookingId(self, arguments=''):
        return max(self.getBookingsIds(arguments))

    def getBookingDetails(self,id):
        url=webServiceAddress+"/booking/%s" %(id)
        resp = requests.get(url)
        if resp.status_code != 200:
            if(resp.status_code == 404):
                raise Exception(("Booking id=%s doesn't exist") % (id))
            else:
                raise Exception('GET /booking/%s {}'.format(resp.status_code) % (id))
        print str(resp.json())
        return resp.json()

    def postBooking(self, booking):
        url=webServiceAddress+"/booking"
        payload = booking
        resp = requests.post(url,json=payload)
        if resp.status_code != 200: # This means something went wrong.
            raise Exception('POST /booking/ {}'.format(resp.status_code))
        print str(resp.json())
        return resp.json()['bookingid']


    def authentication(self,user,password):
        auth_data= {
        "username": user,
        "password": password
        }
        url=webServiceAddress+"/auth"
        resp = requests.post(url, json=auth_data)
        if resp.status_code != 200: # This means something went wrong.
            raise Exception('POST /auth/ {}'.format(resp.status_code))
        else:
            print str(resp.json())
            if('token' in resp.json()):
                token=(resp.json()['token'])
                print "Generated token: "+token
            elif('reason' in resp.json()):
                print "Error: "+str(resp.json()['reason'])
            else:
                raise Exception('POST /auth/ Wrong response')

        return resp.json()

    def putBooking(self,id, booking):
        url=webServiceAddress+"/booking/%s" %(id)
        auth_token=self.authentication("admin","password123")
        payload = booking
        resp = requests.put(url,cookies=auth_token, json=payload)
        if resp.status_code != 405: # This means something went wrong.
            raise Exception('PUT /booking/%s {}'.format(resp.status_code) % (id))
        print str(resp.json())

    def deleteBooking(self,id):
        url=webServiceAddress+"/booking/%s" %(id)
        auth_token=self.authentication("admin","password123")
        resp = requests.delete(url,cookies=auth_token)
        if resp.status_code not in (200,201,204,205):     # expectedcode is 204
            raise Exception('DELETE /booking/%s {}'.format(resp.status_code) % (id))
        return resp.status_code


def main():
    obj = restfulBookerConnection()
    #obj.pingWebService();
    obj.getBookingsIds();
    #obj.postBooking();
    #obj.getBookingsIds();
    #obj.postBooking();
    #obj.getBookingsIds();
    #obj.putBooking('22');
    obj.getBookingDetails(111);
    #obj.authentication("admin","password123")
    #obj.authentication("aaa","aa")
    #obj.getBookingDetails('5');
    obj.deleteBooking('21');
#    obj.deleteBooking('23');
    # obj.getBookings();

if __name__ == "__main__":
    main()
