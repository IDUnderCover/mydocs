LDAP is just a protocol that defines the method by which directory data is accessed.



LDAP DIT　Information 
Each Entry (1) is composed of one or more objectClasses (2)

Each objectClass (2) has a name and is a container for attributes (its definition identifies the attributes it may or must contain)

Each Attribute (3) has a name, contains data, and is a member of one or more objectClass(es) (2)

When the DIT is populated each entry will be uniquely identified (relative to its parent entry) in the hierarchy by the data it contains (in its attributes which are contained in its objectClasses(es)).








http://www.zytrax.com/books/ldap/