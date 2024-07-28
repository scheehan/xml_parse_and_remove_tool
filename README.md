# XML file processing with Python lxml Module

This article were to explain about lxml general functionality and demonstrate how lxml can provide XML content parsing and reading efficiently with the aim to make programmer life easier. lxml consider as one of the most feature-rich and easy-to-use library for processing XML and HTML in the Python language. This article we are going to walk through come of the core feature lxml can provides. lxml package has a quite different way of representing documents as trees.
In the DOM, trees are built out of nodes represented as Node instances.
Some nodes are Element instances, representing whole elements as lists.

![img](/images/lxml_design.png)

Example XML sample file, [sample.xml](sample.xml).



At its most fundamental, XML schema file needs to be [parse][1] and process. We may utilize parse function to quickly convert an XML file into an ElementTree.

**General way to import lxml as etree, and assign xml file name/path as source**

```python
from lxml import etree
tree = etree.parse('sample.xml', parser=etree.XMLParser())
```


**Top Level Element**

```python
print(tree.getroot())
```
Output:
> <Element PurchaseOrders at 0x1fb8c81ed40>

**Element nodes for its element children.** 

```python
print(tree.getroot().getchildren())
```
Output:
> [<Element PurchaseOrder at 0x1dae421eec0>, <Element PurchaseOrder at 0x1dae421f200>, <Element PurchaseOrder at 0x1dae421f2c0>]

**Attribute nodes for its attributes.**

```python
for e in tree.getroot().getchildren():
    print(e.attrib)
```
Output:
> {'PurchaseOrderNumber': '99504', 'OrderDate': '2001-10-20'}  
> {'PurchaseOrderNumber': '99505', 'OrderDate': '2001-10-22'}  
> {'PurchaseOrderNumber': '99503', 'OrderDate': '2001-10-22'}

**Text nodes for textual content.**

```python
for e in tree.getroot().getchildren()[0]:
    print(e.text)
```
Output:
> Please leave packages in shed by driveway.

## XML schema structure 

Each Element has an assortment of child nodes of various types:

![img](/images/xml_element_explained.png)

Supported XML [schema][2] format can refer to below link:

## Serialise XML element objects as string type

Serialize an element to an encoded string representation of its XML tree element.

```python
print(etree.tostring(tree.getroot().getchildren()[0]).decode("utf-8"))
```
Output:
```
<PurchaseOrder PurchaseOrderNumber="99504" OrderDate="2001-10-20">
    <Address Type="Shipping">
      <Name>Amy Adams</Name>
      <Street>123 Maple Street</Street>
      <City>Mill Valley</City>
      <State>CA</State>
      <Zip>10999</Zip>
      <Country>USA</Country>
    </Address>
    <Address Type="Billing">
      <Name>Chong Wei</Name>
      <Street>8 Oak Avenue</Street>
      <City>Old Town</City>
      <State>PA</State>
      <Zip>95819</Zip>
      <Country>USA</Country>
    </Address>
    <DeliveryNotes>Please leave packages in shed by driveway.</DeliveryNotes>
    <Items>
      <Item PartNumber="872-AC">
        <ProductName>Lawnmower</ProductName>
        <Quantity>1</Quantity>
        <USPrice>148.95</USPrice>
        <Comment>Confirm this is electric</Comment>
      </Item>
      <Item PartNumber="926-AD">
        <ProductName>Dell Monitor</ProductName>
        <Quantity>2</Quantity>
        <USPrice>39.98</USPrice>
        <ShipDate>1999-05-21</ShipDate>
      </Item>
    </Items>
  </PurchaseOrder>
```

## XML Content search

lxml provides multiple function to locate ElemenTree (ET) [element path][3]. For this particular demonstration findall seem to be a good fit to locate matching keyword within which child element, and return its index number.

Set search element path 

```python
roottree = tree.getroot()
subelement = roottree[0].tag           # PurchaseOrder
findalltree = tree.findall(subelement)

print(findalltree)
```

> [<Element PurchaseOrder at 0x16675a1f040>, <Element PurchaseOrder at 0x16675a1f380>, <Element PurchaseOrder at 0x16675a1f440>]

Setup search argument and enumeration expression and condition.  
For this particular use case, the objective were to identify interested information reside within which sub-element object. For demonstration purposes, "PartNumber" used as unique keyword to identify sub-element object index id, and sub-element objects.

```python
keyword = 'PartNumber="456-NF"'
for h, i in enumerate(findalltree):

    if keyword in etree.tostring(i).decode("utf-8"):
        
        print(f'index: {h} \n{etree.tostring(i, pretty_print=True).decode("utf-8")}')
```
```
index: 1
<PurchaseOrder PurchaseOrderNumber="99505" OrderDate="2001-10-22">
    <Address Type="Shipping">
      <Name>anna kendrick</Name>
      <Street>456 Main Street</Street>
      <City>Buffalo</City>
      <State>NY</State>
      <Zip>98112</Zip>
      <Country>USA</Country>
    </Address>
    <Address Type="Billing">
      <Name>anna kendrick</Name>
      <Street>456 Main Street</Street>
      <City>Buffalo</City>
      <State>NY</State>
      <Zip>98112</Zip>
      <Country>USA</Country>
    </Address>
    <DeliveryNotes>Please notify me before shipping.</DeliveryNotes>
    <Items>
      <Item PartNumber="456-NF">
        <ProductName>Power Supply</ProductName>
        <Quantity>1</Quantity>
        <USPrice>45.99</USPrice>
      </Item>
    </Items>
  </PurchaseOrder>
```

## Element removal action:

The final product obtained allow us to work on the interested sub-element as we wish. For example, we may use the index number to remove unwanted element.

```python
print(roottree.getchildren())

roottree.remove(findalltree[1])

print(roottree.getchildren())
```

## The Result:

Available sub-elements:
> [<Element PurchaseOrder at 0x23fee01f140>, <Element PurchaseOrder at 0x23fee01f000>, <Element PurchaseOrder at 0x23fee01f3c0>  

Reduced sub-elements after remove sub-element index 1:
> [<Element PurchaseOrder at 0x23fee01f140>, <Element PurchaseOrder at 0x23fee01f3c0>]



[1]: https://lxml.de/apidoc/lxml.etree.html#lxml.etree.parse
[2]: https://www.w3schools.com/XML/schema_schema.asp
[3]: https://lxml.de/tutorial.html#elementpath

---

## Activate virtual environment

```
python -m venv .venv

Windows:
.\.venv\Scripts\activate

Linux & Unix:
source .venv/bin/activate

pip install -r requirements.txt
```