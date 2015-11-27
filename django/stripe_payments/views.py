import stripe

tier_handle_choices = {
                2 :'tier-2',
                3 :'tier-3',
                4 :'tier-4',
                5 :'tier-5',
                6 :'grandfather-trainer',
                7 :'professional'
            }
reverse_tier_handle_choices = {
                 'tier-2' :2,
                 'tier-3' :3,
                 'tier-4' :4,
                 'tier-5' :5,
                 'grandfather-trainer':6,
                 'professional':7,
            }


def get_or_create_customer(self):

    if not self.stripe_id:
        count = 100
        offset = 0
        all_customers_data = stripe.Customer.all(count=count, offset=offset)
        all_customers_bool = all_customers_data.get('has_more')
        all_customers = all_customers_data.get('data')

        while all_customers_bool:

            for customer in all_customers:
                if customer.email == self.email:
                    self.stripe_id = customer.id
                    self.save()
                    return customer

            offset = offset + count
            all_customers_data = stripe.Customer.all(count=count, offset=offset)
            all_customers_bool = all_customers_data.get('has_more')
            all_customers = all_customers_data.get('data')

        for customer in all_customers:
            if customer.email == self.email:
                self.stripe_id = customer.id
                self.save()
                return customer

        response = stripe.Customer.create(
          email=self.email,
        )
        self.stripe_id = response.get('id')
        self.save()
        return response
    else:
        try:
            response = stripe.Customer.retrieve(self.stripe_id)
            if 'deleted' in  response:
                response = stripe.Customer.create(
                  email=self.email,
                )
                self.stripe_id = response.get('id')
        except stripe.error.InvalidRequestError:
            response = stripe.Customer.create(
                  email=self.email,
                )
            self.stripe_id = response.get('id')
        try:
            response.metadata['training-with'] = self.referred_by.email
        except:
            #referred by rory
            response.metadata['training-with'] = 'rory@heavenly-homes.com'
        response.save()
        self.save()
        return response


def delete_customer(self):
    customer1 = self.stripe_get_or_create_customer()
    customer2 = stripe.Customer.retrieve(self.stripe_id)
    if customer1 == customer2:
        customer1.delete()
    return


def get_or_create_creditcard(self, stripToken):
    customer = self.stripe_get_or_create_customer()
    default_card =  customer.default_card

    if default_card:
        card = customer.cards.retrieve(default_card)
    else:
        try:
            card =customer.cards.create(card=stripToken)
        except Exception as e:
            return {'creditcard':str(e)}
    return card


def edit_creditcard(self, stripToken):
    customer = self.stripe_get_or_create_customer()
    old_card = customer.default_card
    try:
        card = customer.cards.create(card=stripToken)
    except Exception as e:
        print e
        return {'creditcard':str(e)}

    customer.default_card = card
    if old_card:
        customer.cards.retrieve(old_card).delete()


def get_creditcard(self):
    customer = self.stripe_get_or_create_customer()
    default_card =  customer.default_card
    if default_card:
        card = customer.cards.retrieve(default_card)
        return card
    else:
        return


def delete_creditcard(self):
    customer = self.stripe_get_or_create_customer()
    default_card = customer.default_card
    if default_card:
        customer.cards.retrieve(default_card).delete()


def update_subscription(self):
    global reverse_tier_handle_choices
    if self.tier == 1:
        return

    customer = self.stripe_get_or_create_customer()
    subscriptions = customer.subscriptions.all(limit=3)
    if not subscriptions.data:
        tier_handle = tier_handle_choices[self.tier]
        customer.subscriptions.create(plan=tier_handle)
        return
    else:
        tier_handle = tier_handle_choices[self.tier]
        subscription = subscriptions.data[0]
        subscription.plan = tier_handle
        subscription.save()
        return


def cancel_subscription(self):
    customer = self.stripe_get_or_create_customer()
    subscriptions = customer.subscriptions.all(limit=3)
    try:
        subscription = subscriptions.data[0]
        subscription.plan = 'cancel-subscription'
        subscription.save()
        subscription.delete()
    except:
        pass


