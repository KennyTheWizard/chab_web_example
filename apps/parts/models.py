from django.db import models

# Create your models here.
class PartManager(models.Manager):

    def add_subpart(self, parent_id, child_id, quantity):
        parent = self.get(id=parent_id)
        child = self.get(id=child_id)
        if quantity == '':
            return {'message' : 'Quantity cannot be blank.'}
        if float(quantity) <= 0:
            return {'message' : 'Quantity must be positive.'}
        if parent and child:
            if parent.id == child.id or child.check_all_children(parent):
                return { 'message' : 'Part cannot be subpart of itself' }
            SubPart.objects.create(
                parent=parent,
                child=child,
                quantity=quantity,
            )
            return { 'status':True, 'message':'Relationship made'}
    def remove_subpart(self, parent_id, child_id):
        parent = self.get(id=parent_id)
        child = self.get(id=child_id)
        relation = SubPart.objects.filter(parent=parent, child=child)
        if relation:
            relation.delete()
            return {'status' : True, 'message' : 'Child removed'}
        return {'status' : False, 'message' : 'No relationship'}


    def recursive_children(self, part):
        ret_arr = []
        #print(part.name)
        for sub in part.children.all():
            child_json = {}
            #print(part.name, sub.child.name)
            child_json['id'] = '{}_{}'.format(part.id, sub.child.id)
            child_json['text'] = 'Name: {} Qty: {}'.format(
                sub.child.name, sub.quantity)
            if sub.child.children.all():
                child_json['children'] = self.recursive_children(sub.child)
            ret_arr.append(child_json)
        return ret_arr

    def get_flat_json(self, searchstring):
        ret_arr = []
        for part in self.filter(name__icontains=searchstring):
            part_json = {
                'id' : part.id,
                'name' : part.name,
            }
            ret_arr.append(part_json)
        return ret_arr

    def get_tree_json(self, searchstring):
        the_parts = self.filter(name__icontains=searchstring)
        ret_arr = []
        for part in the_parts:
            part_json = {}
            part_json['id'] = str(part.id)
            part_json['text'] = 'Name: {}'.format(part.name,)
            subparts = part.children.all()
            # for subpart in subparts:
            #     print(part.name, subpart.child.name)
            # print(subparts)
            if subparts:
                part_json['children'] = self.recursive_children(part)
            ret_arr.append(part_json)
        return ret_arr

    def add_new_part(self, post_data):
        response = {}
        # add regex for partname
        # if post_data['manufacturer']:
        #     the_manufact = post_data['manufacturer']
        #     new_manufact = False
        # elif post_data['new_manufacturer']:
        #     the_manufact = Manufacturer.objects.filter(
        #         name=post_data['new_manufacturer'])
        #     if the_manufact:
        #         the_manufact = the_manufact[0]
        #     else:
        #         the_manufact = Manufacturer.objects.create(
        #             name=post_data['new_manufacturer']
        #         )
        #         new_manufact = True
        # else:
        #     response['status'] = False
        #     response['manufacturer'] = "You must select a manufacturer or add a new one."

        check_part = self.filter(name=post_data['part_name'])
        if check_part:
            response['status'] = False
            response['part'] = 'Part already added'
            return response
        new_part = self.create(
            name=post_data['part_name'],
            is_divisible=post_data['is_divisible'],
            desc=post_data['part_desc'],
        )
        response['status'] = True
        response['new_part'] = new_part
        return response
    def update_part(self, part_id, post_data):
        response = {}
        edit_part = self.filter(id=part_id)
        if not edit_part:
            response['status'] = False
            response['message'] = 'Part Not Found'
            return response
        name_conflicts = self.filter(name=post_data['part_name']).exclude(id=part_id)
        if name_conflicts:
            response['status'] = False
            response['message'] = 'Part name in use'
            return response
        edit_part.update(
            name=post_data['part_name'],
            desc=post_data['part_desc'],
            is_divisible=post_data['is_divisible']
        )
        response['status'] = True
        response['message'] = 'Part id: {} updated'.format(edit_part[0].id)
        return response

    def delete_part(self, post_data):
        del_part = self.filter(id=post_data['part_id'])
        if del_part:
            del_part.delete()
            return {'status':True}
        return {'status':False}
# class Manufacturer(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     def __str__(self):
#         return self.name

class Part(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    is_divisible = models.BooleanField()
    subpart = models.ManyToManyField(
        'self',
        related_name='subparts',
        through='SubPart',
        through_fields=['parent', 'child'],
        symmetrical=False,
    )
    # manufacturer = models.ForeignKey(Manufacturer, related_name='parts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PartManager()

    def check_all_children(self, parent):
        my_children = self.children.all()
        #print(parent, self, my_children)
        their_parents = my_children.filter(child=parent)
        print(their_parents)
        if their_parents:
            return True
        for a_child in my_children:
            print(parent.name)
            print(a_child.child.name)
            return a_child.child.check_all_children(parent)
        return False


# class Cost(models.Model):
#     cost = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='costs')

class SubPart(models.Model):
    parent = models.ForeignKey(Part, related_name='children')
    child = models.ForeignKey(Part, related_name='parents')
    quantity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
