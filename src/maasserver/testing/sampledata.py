# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Construct sample application data dynamically."""

__all__ = [
    "populate",
]

import random
from socket import gethostname
from textwrap import dedent

from maasserver.enum import (
    ALLOCATED_NODE_STATUSES,
    INTERFACE_TYPE,
    IPADDRESS_TYPE,
    NODE_STATUS,
    NODE_TYPE,
)
from maasserver.models import (
    Domain,
    Fabric,
    Node,
    VersionedTextFile,
)
from maasserver.storage_layouts import STORAGE_LAYOUTS
from maasserver.testing.factory import factory
from maasserver.utils.orm import (
    get_one,
    transactional,
)
from provisioningserver.utils.enum import map_enum
from provisioningserver.utils.ipaddr import get_mac_addresses


class RandomInterfaceFactory:

    @classmethod
    def create_random(cls, node):
        """Create a random interface configuration for `node`."""
        creator = random.choice([
            cls._create_basic,
            cls._create_bond,
            cls._create_vlan,
            cls._create_bond_vlan,
        ])
        creator(node)

    @classmethod
    def _create_basic(cls, node, fabric=None, assign_ips=True):
        """Create 3 physical interfaces on `node`."""
        interfaces = []
        for _ in range(3):
            if fabric is None:
                fabric = random.choice(list(Fabric.objects.all()))
            vlan = fabric.get_default_vlan()
            interface = factory.make_Interface(
                INTERFACE_TYPE.PHYSICAL, node=node, vlan=vlan)
            interfaces.append(interface)
            if assign_ips:
                cls.assign_ip(interface)
        return interfaces

    @classmethod
    def _create_bond(cls, node):
        """Create a bond interface from the 3 created physical interfaces."""
        fabric = random.choice(list(Fabric.objects.all()))
        vlan = fabric.get_default_vlan()
        parents = cls._create_basic(node, fabric=fabric, assign_ips=False)
        bond = factory.make_Interface(
            INTERFACE_TYPE.BOND, node=node, vlan=vlan, parents=parents)
        cls.assign_ip(bond)
        return bond

    @classmethod
    def _create_vlan(cls, node, parents=None):
        """Create a VLAN interface one for each of the 3 created physical
        interfaces."""
        interfaces = []
        if parents is None:
            parents = cls._create_basic(node)
        for parent in parents:
            tagged_vlans = list(
                parent.vlan.fabric.vlan_set.exclude(id=parent.vlan.id))
            if len(tagged_vlans) > 0:
                vlan = random.choice(tagged_vlans)
            else:
                vlan = factory.make_VLAN(fabric=parent.vlan.fabric)
            vlan_interface = factory.make_Interface(
                INTERFACE_TYPE.VLAN, node=node, vlan=vlan, parents=[parent])
            interfaces.append(vlan_interface)
            cls.assign_ip(vlan_interface)
        return interfaces

    @classmethod
    def _create_bond_vlan(cls, node):
        """Create a bond interface with a VLAN interface on that bond."""
        bond = cls._create_bond(node)
        cls._create_vlan(node, parents=[bond])

    @classmethod
    def assign_ip(cls, interface, alloc_type=None):
        """Assign an IP address to the interface.
        """
        subnets = list(interface.vlan.subnet_set.all())
        if len(subnets) > 0:
            subnet = random.choice(subnets)
            if alloc_type is None:
                alloc_type = random.choice(
                    [IPADDRESS_TYPE.STICKY, IPADDRESS_TYPE.AUTO])
            if (alloc_type == IPADDRESS_TYPE.AUTO and
                    interface.node.status not in [
                        NODE_STATUS.DEPLOYING,
                        NODE_STATUS.DEPLOYED,
                        NODE_STATUS.FAILED_DEPLOYMENT,
                        NODE_STATUS.RELEASING]):
                assign_ip = ""
            else:
                # IPv6 use pick_ip_in_network as pick_ip_in_Subnet takes
                # forever with the IPv6 network.
                network = subnet.get_ipnetwork()
                if network.version == 6:
                    assign_ip = factory.pick_ip_in_network(network)
                else:
                    assign_ip = factory.pick_ip_in_Subnet(subnet)
            factory.make_StaticIPAddress(
                alloc_type=alloc_type,
                subnet=subnet,
                ip=assign_ip,
                interface=interface)


@transactional
def populate(seed="sampledata"):
    """Populate the database with example data.

    This should:

    - Mimic a real-world MAAS installation,

    - Create example data for all of MAAS's features,

    - Not go overboard; in general there need be at most a handful of each
      type of object,

    - Have elements of randomness; the sample data should never become
      something we depend upon too closely — for example in QA, demos, and
      tests — and randomness helps to keep us honest.

    If there is something you need, add it. If something does not make sense,
    change it or remove it. If you need something esoteric that would muddy
    the waters for the majority, consider putting it in a separate function.

    This function expects to be run into an empty database. It is not
    idempotent, and will almost certainly crash if invoked multiple times on
    the same database.

    """
    random.seed(seed)

    admin = factory.make_admin(username="admin", password="test")  # noqa
    user1, _ = factory.make_user_with_keys(username="user1", password="test")
    user2, _ = factory.make_user_with_keys(username="user2", password="test")

    # Physical zones.
    zones = [
        factory.make_Zone(name="zone-north"),
        factory.make_Zone(name="zone-south"),
    ]

    # DNS domains.
    domains = [
        Domain.objects.get_default_domain(),
        factory.make_Domain("sample"),
        factory.make_Domain("ubnt"),
    ]

    # Create the fabrics that will be used by the regions, racks,
    # machines, and devices.
    fabric0 = Fabric.objects.get_default_fabric()
    fabric0_untagged = fabric0.get_default_vlan()
    fabric0_vlan10 = factory.make_VLAN(fabric=fabric0, vid=10)
    fabric1 = factory.make_Fabric()
    fabric1_untagged = fabric1.get_default_vlan()
    fabric1_vlan42 = factory.make_VLAN(fabric=fabric1, vid=42)
    empty_fabric = factory.make_Fabric()  # noqa

    # Create some spaces.
    space_mgmt = factory.make_Space("management")
    space_storage = factory.make_Space("storage")
    space_internal = factory.make_Space("internal")
    space_ipv6_testbed = factory.make_Space("ipv6-testbed")

    # Subnets used by regions, racks, machines, and devices.
    subnet_1 = factory.make_Subnet(
        cidr="172.16.1.0/24", gateway_ip="172.16.1.1",
        vlan=fabric0_untagged, space=space_mgmt)
    subnet_2 = factory.make_Subnet(
        cidr="172.16.2.0/24", gateway_ip="172.16.2.1",
        vlan=fabric1_untagged, space=space_mgmt)
    subnet_3 = factory.make_Subnet(
        cidr="172.16.3.0/24", gateway_ip="172.16.3.1",
        vlan=fabric0_vlan10, space=space_storage)
    subnet_4 = factory.make_Subnet(  # noqa
        cidr="172.16.4.0/24", gateway_ip="172.16.4.1",
        vlan=fabric0_vlan10, space=space_internal)
    subnet_2001_db8_42 = factory.make_Subnet(  # noqa
        cidr="2001:db8:42::/64", gateway_ip="",
        vlan=fabric1_vlan42, space=space_ipv6_testbed)

    # Static routes on subnets.
    factory.make_StaticRoute(source=subnet_1, destination=subnet_2)
    factory.make_StaticRoute(source=subnet_1, destination=subnet_3)
    factory.make_StaticRoute(source=subnet_1, destination=subnet_4)
    factory.make_StaticRoute(source=subnet_2, destination=subnet_1)
    factory.make_StaticRoute(source=subnet_2, destination=subnet_3)
    factory.make_StaticRoute(source=subnet_2, destination=subnet_4)
    factory.make_StaticRoute(source=subnet_3, destination=subnet_1)
    factory.make_StaticRoute(source=subnet_3, destination=subnet_2)
    factory.make_StaticRoute(source=subnet_3, destination=subnet_4)
    factory.make_StaticRoute(source=subnet_4, destination=subnet_1)
    factory.make_StaticRoute(source=subnet_4, destination=subnet_2)
    factory.make_StaticRoute(source=subnet_4, destination=subnet_3)

    hostname = gethostname()
    region_rack = get_one(Node.objects.filter(
        node_type=NODE_TYPE.REGION_AND_RACK_CONTROLLER, hostname=hostname))
    # If "make run" executes before "make sampledata", the rack may have
    # already registered.
    if region_rack is None:
        region_rack = factory.make_Node(
            node_type=NODE_TYPE.REGION_AND_RACK_CONTROLLER,
            hostname=hostname, interface=False)

        # Get list of mac addresses that should be used for the region
        # rack controller. This will make sure the RegionAdvertisingService
        # picks the correct region on first start-up and doesn't get multiple.
        mac_addresses = get_mac_addresses()

        def get_next_mac():
            try:
                return mac_addresses.pop()
            except IndexError:
                return factory.make_mac_address()

        # Region and rack controller (hostname of dev machine)
        #   eth0     - fabric 0 - untagged
        #   eth1     - fabric 0 - untagged
        #   eth2     - fabric 1 - untagged - 172.16.2.2/24 - static
        #   bond0    - fabric 0 - untagged - 172.16.1.2/24 - static
        #   bond0.10 - fabric 0 - 10       - 172.16.3.2/24 - static
        eth0 = factory.make_Interface(
            INTERFACE_TYPE.PHYSICAL, name="eth0",
            node=region_rack, vlan=fabric0_untagged,
            mac_address=get_next_mac())
        eth1 = factory.make_Interface(
            INTERFACE_TYPE.PHYSICAL, name="eth1",
            node=region_rack, vlan=fabric0_untagged,
            mac_address=get_next_mac())
        eth2 = factory.make_Interface(
            INTERFACE_TYPE.PHYSICAL, name="eth2",
            node=region_rack, vlan=fabric1_untagged,
            mac_address=get_next_mac())
        bond0 = factory.make_Interface(
            INTERFACE_TYPE.BOND, name="bond0",
            node=region_rack, vlan=fabric0_untagged,
            parents=[eth0, eth1], mac_address=eth0.mac_address)
        bond0_10 = factory.make_Interface(
            INTERFACE_TYPE.VLAN, node=region_rack,
            vlan=fabric0_vlan10, parents=[bond0])
        factory.make_StaticIPAddress(
            alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.1.2",
            subnet=subnet_1, interface=bond0)
        factory.make_StaticIPAddress(
            alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.2.2",
            subnet=subnet_2, interface=eth2)
        factory.make_StaticIPAddress(
            alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.3.2",
            subnet=subnet_3, interface=bond0_10)

    # Rack controller (happy-rack)
    #   eth0     - fabric 0 - untagged
    #   eth1     - fabric 0 - untagged
    #   eth2     - fabric 1 - untagged - 172.16.2.3/24 - static
    #   bond0    - fabric 0 - untagged - 172.16.1.3/24 - static
    #   bond0.10 - fabric 0 - 10       - 172.16.3.3/24 - static
    rack = factory.make_Node(
        node_type=NODE_TYPE.RACK_CONTROLLER,
        hostname="happy-rack", interface=False)
    eth0 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth0",
        node=rack, vlan=fabric0_untagged)
    eth1 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth1",
        node=rack, vlan=fabric0_untagged)
    eth2 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth2",
        node=rack, vlan=fabric1_untagged)
    bond0 = factory.make_Interface(
        INTERFACE_TYPE.BOND, name="bond0",
        node=rack, vlan=fabric0_untagged, parents=[eth0, eth1])
    bond0_10 = factory.make_Interface(
        INTERFACE_TYPE.VLAN, node=rack,
        vlan=fabric0_vlan10, parents=[bond0])
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.1.3",
        subnet=subnet_1, interface=bond0)
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.2.3",
        subnet=subnet_2, interface=eth2)
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.3.3",
        subnet=subnet_3, interface=bond0_10)

    # Region controller (happy-region)
    #   eth0     - fabric 0 - untagged
    #   eth1     - fabric 0 - untagged
    #   eth2     - fabric 1 - untagged - 172.16.2.4/24 - static
    #   bond0    - fabric 0 - untagged - 172.16.1.4/24 - static
    #   bond0.10 - fabric 0 - 10       - 172.16.3.4/24 - static
    region = factory.make_Node(
        node_type=NODE_TYPE.REGION_CONTROLLER,
        hostname="happy-region", interface=False)
    eth0 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth0",
        node=region, vlan=fabric0_untagged)
    eth1 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth1",
        node=region, vlan=fabric0_untagged)
    eth2 = factory.make_Interface(
        INTERFACE_TYPE.PHYSICAL, name="eth2",
        node=region, vlan=fabric1_untagged)
    bond0 = factory.make_Interface(
        INTERFACE_TYPE.BOND, name="bond0",
        node=region, vlan=fabric0_untagged, parents=[eth0, eth1])
    bond0_10 = factory.make_Interface(
        INTERFACE_TYPE.VLAN, node=region,
        vlan=fabric0_vlan10, parents=[bond0])
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.1.4",
        subnet=subnet_1, interface=bond0)
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.2.4",
        subnet=subnet_2, interface=eth2)
    factory.make_StaticIPAddress(
        alloc_type=IPADDRESS_TYPE.STICKY, ip="172.16.3.4",
        subnet=subnet_3, interface=bond0_10)

    # Create one machine for every status. Each machine has a random interface
    # and storage configration.
    node_statuses = [
        status
        for status in map_enum(NODE_STATUS).items()
        if status not in [
            NODE_STATUS.MISSING,
            NODE_STATUS.RESERVED,
            NODE_STATUS.RETIRED]
    ]
    for _, status in node_statuses:
        owner = None
        if status in ALLOCATED_NODE_STATUSES:
            owner = random.choice([admin, user1, user2])
        elif status in [
                NODE_STATUS.COMMISSIONING,
                NODE_STATUS.FAILED_RELEASING]:
            owner = admin
        machine = factory.make_Node(
            status=status, owner=owner, zone=random.choice(zones),
            interface=False, with_boot_disk=False, power_type='manual',
            domain=random.choice(domains))
        machine.set_random_hostname()

        # Create random network configuration.
        RandomInterfaceFactory.create_random(machine)

        # Add random storage devices and set a random layout.
        for _ in range(3):
            factory.make_PhysicalBlockDevice(node=machine)
        if status in [
                NODE_STATUS.READY,
                NODE_STATUS.ALLOCATED,
                NODE_STATUS.DEPLOYING,
                NODE_STATUS.DEPLOYED,
                NODE_STATUS.FAILED_DEPLOYMENT,
                NODE_STATUS.RELEASING,
                NODE_STATUS.FAILED_RELEASING]:
            machine.set_storage_layout(
                random.choice(list(STORAGE_LAYOUTS.keys())))
            if status != NODE_STATUS.READY:
                machine._create_acquired_filesystems()

        # Add a random amount of events.
        for _ in range(random.randint(25, 100)):
            factory.make_Event(node=machine)

        # Add installation results.
        if status in [
                NODE_STATUS.DEPLOYING,
                NODE_STATUS.DEPLOYED,
                NODE_STATUS.FAILED_DEPLOYMENT]:
            script_result = 0
            if status == NODE_STATUS.FAILED_DEPLOYMENT:
                script_result = 1
            factory.make_NodeResult_for_installation(
                node=machine, script_result=script_result,
                name="curtin.log", data=factory.make_string().encode("ascii"))

        # Add children devices to the deployed machine.
        if status == NODE_STATUS.DEPLOYED:
            boot_interface = machine.get_boot_interface()
            for _ in range(5):
                device = factory.make_Device(
                    interface=True, domain=machine.domain, parent=machine,
                    vlan=boot_interface.vlan)
                device.set_random_hostname()
                RandomInterfaceFactory.assign_ip(
                    device.get_boot_interface(),
                    alloc_type=IPADDRESS_TYPE.STICKY)

    # Create a few devices.
    for _ in range(10):
        device = factory.make_Device(interface=True)
        device.set_random_hostname()

    # Add some DHCP snippets.
    # - Global
    factory.make_DHCPSnippet(
        name="foo class", description="adds class for vender 'foo'",
        value=VersionedTextFile.objects.create(data=dedent("""\
            class "foo" {
                match if substring (
                    option vendor-class-identifier, 0, 3) = "foo";
            }
        """)))
    factory.make_DHCPSnippet(
        name="bar class", description="adds class for vender 'bar'",
        value=VersionedTextFile.objects.create(data=dedent("""\
            class "bar" {
                match if substring (
                    option vendor-class-identifier, 0, 3) = "bar";
            }
        """)), enabled=False)
    # - Subnet
    factory.make_DHCPSnippet(
        name="600 lease time", description="changes lease time to 600 secs.",
        value=VersionedTextFile.objects.create(data="default-lease-time 600;"),
        subnet=subnet_1)
    factory.make_DHCPSnippet(
        name="7200 max lease time",
        description="changes max lease time to 7200 secs.",
        value=VersionedTextFile.objects.create(data="max-lease-time 7200;"),
        subnet=subnet_2, enabled=False)
    # - Node
    factory.make_DHCPSnippet(
        name="boot from other server",
        description="instructs device to boot from other server",
        value=VersionedTextFile.objects.create(data=dedent("""\
            filename "test-boot";
            server-name "boot.from.me";
        """)), node=device)
