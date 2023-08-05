import requests
import json
import uuid
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
Add Tier0 router (not VRF)
Add Tier 1 router
Change BGP AS
Add BGP Peer 
Add BGP Peer protocol families
Add uplinks to router
Add IPv6 subnet/DHCP to segment 
Gather more information from platform for Fact 
Get BGP neighbour status (get_bgp_neighbor, get_bgp_summary)

'''


class device:
	def __init__(self,host,user,password,router):
		self.host = host
		self.user = user
		self.password = password
		self.router = router
		info = self.open()
		self.locale_path = self.get_locale_path(self.router)
		self.router_id = info[0]
		self.headers = {'Content-Type': 'application/json'}
				
	def error(self,code):
		if code == 301:
			response = {'Moved Permanently'}
		elif code == 307:
			response = {'Temporary Redirect'}
		elif code == 400:
			response = {'Bad Request'}
		elif code == 403:
			response = {'Forbidden'}
		elif code == 409:
			response = {'Conflict'}	
		elif code == 500:
			response = {'Internal Service Error'}
		elif code == 503:
			response = {'Service Unavailable'}		
		return response

	def open(self):
		json_response = requests.get('https://'+self.host+'/policy/api/v1/infra/tier-0s/', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			#generates a list of dictionaries for the return content
			response = json.loads(json_response.content)
			response = response["results"]
			for t0 in response:
				if t0['display_name'] == self.router:
					response = t0['rd_admin_field'],t0['resource_type']
		else:
			response = self.error(json_response.status_code)
		return response
		
	def get_config(self):
	#Pass the name of the transport zone and return the URL path 
		json_response = requests.get('https://'+self.host+'/policy/api/v1/infra?filter=Type-', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response				
		
		

	def get_transport_zone_path(self,tz):
	#Pass the name of the transport zone and return the URL path 
		json_response = requests.get('https://'+self.host+'/policy/api/v1/infra/sites/default/enforcement-points/default/transport-zones', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
			for zone in response:
				if zone['display_name'] == tz:
					response = zone['path']
		else:
			response = self.error(json_response.status_code)
		return response		
		
		
	def get_edge_cluster_path(self,cluster):
	#Pass the name of the transport zone and return which edge cluster path it is connected to. 
		json_response = requests.get('https://'+self.host+'/policy/api/v1/infra/sites/default/enforcement-points/default/edge-clusters/', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
			for value in response:
				if value['display_name'] == cluster:
					response = value['path']
		else:
			response = self.error(json_response.status_code)
		return response		
		
	def get_locale_path(self,router):
	#Pass the name of the T0 router and return the locale-path URI. 
		json_response = requests.get('https://'+self.host+'/policy/api/v1/infra/tier-0s/'+router+'/locale-services', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
			for value in response:
					response = value['path']
		else:
			response = self.error(json_response.status_code)
		return response	
		
	def get_bgp_peer_id(self,neighbor):
	#Pass the name of the T0 router and return the locale-path URI. 
		json_response = requests.get('https://'+self.host+'/policy/api/v1' + self.locale_path +'/bgp/neighbors', verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
			for value in response:
				if value['neighbor_address'] == neighbor:
					response = value['id']
		else:
			response = self.error(json_response.status_code)
		return response		
		
#Route table operations 
		
	def get_route_table(self, router):	
		#edge_path = self.get_edge_cluster_path(vrf)	
		#print(edge_path)
		json_response = requests.get('https://'+ self.host +'/policy/api/v1/infra/tier-0s/' + router + '/routing-table', verify=False, auth=(self.user, self.password))	
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
		else:
			response = self.error(json_response.status_code)
		return response				


#Routing instances (Tier0 VRF's EVPN instances )

	def get_routing_instance(self,vrf_name):
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response	

	def set_routing_instance(self,vrf_name,rt,rd,vni):
		vrf = {'vrf_config': {"tier0_path": "/infra/tier-0s/" + self.router,"route_targets": [{"address_family": "L2VPN_EVPN","import_route_targets": [rt],"export_route_targets": [rt]}],"route_distinguisher": self.router_id + ":" +rd,"evpn_transit_vni": vni}}
		vrf_json = json.dumps(vrf)
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name
		json_response = requests.request("PATCH", url, data = vrf_json, headers=self.headers, verify=False, auth=(self.user, self.password))
		print(json_response.text.encode('utf8'))
		if json_response.status_code == 200:
			response = self.get_routing_instance(vrf_name)
		else:
			response = self.error(json_response.status_code)
		return response

	def del_routing_instance(self,vrf_name):
		self.del_route_policy(vrf_name)
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name
		json_response = requests.request("DELETE", url, verify=False, auth=(self.user, self.password))
		#print("VRF deleted")

#BGP operations 

	def get_bgp_summary(self):
		url = "https://" + self.host + '/policy/api/v1' + self.locale_path + '/bgp'
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response	

	def get_bgp_neighbors(self):
		url = "https://" + self.host + '/policy/api/v1' + self.locale_path + '/bgp/neighbors'
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response
		
	def get_bgp_received_routes(self,peer):
		self.id = self.get_bgp_peer_id(peer)
		url = "https://" + self.host + '/policy/api/v1' + self.locale_path + '/bgp/neighbors/' + self.id + '/routes'
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response

	def get_bgp_advertised_routes(self,peer):
		self.id = self.get_bgp_peer_id(peer)
		url = "https://" + self.host + '/policy/api/v1' + self.locale_path + '/bgp/neighbors/' + self.id + '/advertised-routes'
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response
		
		
#Networks (aka Segments)

	def get_network(self,network_name):
		url = "https://" + self.host + "/policy/api/v1/infra/segments/" + network_name
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response
		
	def set_network(self,network_name,gateway,mask,vrf_name, tz):
		tz_path = self.get_transport_zone_path(tz)
		segment = {'subnets': [{'gateway_address': gateway+"/"+mask}],"transport_zone_path": tz_path,"admin_state":"UP", 'connectivity_path': '/infra/tier-0s/'+vrf_name,"advanced_config":{"address_pool_paths":[]},"dhcp_config_path":"/infra/dhcp-server-configs/DHCP_6","id": network_name }
		segment_json = json.dumps(segment)		
		url = "https://" + self.host + "/policy/api/v1/infra/segments/" + network_name
		response = requests.request("PATCH", url, data = segment_json, headers=self.headers, verify=False, auth=(self.user, self.password))
		print(response.text.encode('utf8'))
		print("Network created and attached")
				
	def del_network(self,network_name):
		url = "https://" + self.host + "/policy/api/v1/infra/segments/" + network_name
		response = requests.request("DELETE", url, verify=False, auth=(self.user, self.password))
		#print("Network deleted")


#Routing policy (part of locale Services)

	def get_route_policy(self,vrf_name):
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name + "/locale-services"
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		response = json.loads(json_response.content)
		response = response["results"]
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response
			
	def set_route_policy(self,policy_name, vrf_name,type):
		id = uuid.uuid4()
		redist = {'route_redistribution_config': {'redistribution_rules': [{'name': policy_name, 'route_redistribution_types': ['TIER0_CONNECTED', 'TIER1_CONNECTED']}]}}
		redist_json = json.dumps(redist)
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name  + "/locale-services/" + str(id)
		response = requests.request("PUT", url, data = redist_json, headers=self.headers, verify=False, auth=(self.user, self.password))
		print(response.text.encode('utf8'))
		
	def del_route_policy(self,vrf_name):
		url = "https://" + self.host + "/policy/api/v1/infra/tier-0s/" + vrf_name + "/locale-services"
		rest_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		response = json.loads(rest_response.content)
		response = response["results"]
		for entry in response:
			path = entry['path']
			#print(path)
			url = "https://" + self.host + "/policy/api/v1" + path
			response = requests.request("DELETE", url, headers=self.headers, verify=False, auth=(self.user, self.password))		

#Retrieve Virtual Machine information

	def get_virtual_machines(self):
		url = "https://" + self.host + "/policy/api/v1/infra/realized-state/virtual-machines"
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
		else:
			response = self.error(json_response.status_code)
		return response

	def get_virtual_machine_id(self,vm_name):
		url = "https://" + self.host + "/policy/api/v1/infra/realized-state/virtual-machines"
		json_response = requests.request("GET", url, headers=self.headers, verify=False, auth=(self.user, self.password))
		if json_response.status_code == 200:
			response = json.loads(json_response.content)
			response = response["results"]
			for value in response:
				if value['display_name'] == vm_name:
					response = value['external_id']	
		else:
			response = "Not Found"
		return response	
		
			
#Tag Virtual Machines

	def set_virtual_machine_tag(self,vm_name, tag_name, scope):
		id = uuid.uuid4()
		vm_id = self.get_virtual_machine_id(vm_name)
		tag = {'tag': {'scope': scope, 'tag': tag_name },'apply_to': [{'resource_type': 'VirtualMachine','resource_ids':[ vm_id]}]}
		tag_json = json.dumps(tag)
		url = "https://" + self.host + "/policy/api/v1/infra/tags/tag-operations/"+str(id)
		response = requests.request("PUT", url, data = tag_json, headers=self.headers, verify=False, auth=(self.user, self.password))
		#print(response.text.encode('utf8'))
		
	def del_virtual_machine_tag(self,vm_name, tag_name, scope):
		id = uuid.uuid4()
		vm_id = self.get_virtual_machine_id(vm_name)
		tag = {'tag': {'scope': scope, 'tag': tag_name },'remove_from': [{'resource_type': 'VirtualMachine','resource_ids':[ vm_id]}]}
		tag_json = json.dumps(tag)
		url = "https://" + self.host + "/policy/api/v1/infra/tags/tag-operations/"+str(id)
		response = requests.request("PUT", url, data = tag_json, headers=self.headers, verify=False, auth=(self.user, self.password))
		#print(response.text.encode('utf8'))

		
