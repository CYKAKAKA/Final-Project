class Order:
    """

    This is a class for order definition.

    Attributes:
        time (int): The time when the restaurant receive an order.
        size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
        preparation_time (double): The time need for preparation
        order_location (tuple): The coordinate of the location of the order
        delivery_time (double): The time spend on the way to destination
        supposed_delivered_time(int): The time when the order should be delivered
        delivered_time (double): The time when the order arrives
        status (string): to define whether the order is cancelled
        mark (int): The job number of delivery man who delivers the order

    """
    def __init__(self, time, size, preparation_time=0, order_location=(0, 1), delivery_time=0,
                 supposed_delivered_time=0, delivered_time=0, status=0, mark=0):

        """
        The constructor for ComplexNumber class.

        Parameters:
            time (int): The time when the restaurant receive an order.
            size (int): 1 stands for small; 2 stands for medium and 3 stands for large.
            preparation_time (double): The time need for preparation
            order_location (tuple): The coordinate of the location of the order
            delivery_time (double): The time spend on the way to destination
            supposed_delivered_time(int): The time when the order should be delivered
            delivered_time (double): The time when the order arrives
            status (string): to define whether the order is cancelled
            mark (int): The job number of delivery man who delivers the order
        """
        self.time = time
        self.size = size
        self.preparation_time = preparation_time
        self.order_location = order_location
        self.mark = mark
        self.delivered_time = delivered_time
        self.delivery_time = delivery_time
        self.supposed_delivered_time = supposed_delivered_time
        self.Status = status

    def set_preparation_time(self):
        """
        The function is to set the preparation time for an Order

        """
        self.preparation_time = 10
        if self.size == 1:
            pass
        elif self.size == 2:
            self.preparation_time *= 1.5
        else:
            self.preparation_time *= 2

    def set_order_location(self, length, width, i):
        """
        The function is to set the order location for an Order

        Parameters:
           length (int)：the length of the map
           width (int): the width of the map
           i: a randomly generated number
        """

        order_location = list(real_map(mapping(length,width)).nodes)[i]

        self.order_location = order_location

    def set_delivery_time(self, restaurant_loc, mapgrid):
        """
        The function is to set the delivery time for an Order

        Parameters:
           restaurant_loc (int)：the coordinate of the restaurant
           mapgrid (int): the map
        """

        delivery_time = nx.dijkstra_path_length(mapgrid, source=restaurant_loc, target=self.order_Location,
                                                weight='time')

        self.delivery_time = delivery_time

    def set_supposed_delivered_time(self):
        """
        The function is to set the supposed delivered time for an Order

        """

        supposed_delivered_time = self.time + 100

        self.supposed_delivered_time = supposed_delivered_time

    def set_delivered_time(self, delivered_time):

        self.delivered_time = delivered_time

    def set_status(self):
        """
        The function is to set status for an Order

        Parameters:

        """

        if self.delivered_time < self.supposed_delivered_time:
            self.Status = 'processing'
        else:
            self.Status = 'cancelled'

    def set_mark(self, mark):
        """
        The function is to set mark for an Order

        Parameters:
            mark (int): the job number of a delivery man
        """

        self.mark = mark


class DeliveryMan:
    """

        This is a class for delivery man definition.

        Attributes:
            job_number (int): The time when the restaurant receive an order.
            arrived_time( double): The time when a delivery man return to the restaurant

    """

    def __init__(self, job_number, arrived_time=0):
        """
        The constructor for ComplexNumber class.

        Parameters:
            job_number (int): The time when the restaurant receive an order.
            arrived_time( double): The time when a delivery man return to the restaurant

        """
        self.job_number = job_number
        self.arrived_time = arrived_time

    def set_arrived_time(self, delivered_time, delivery_time):
        """
        The function is to set mark for an Order

        Parameters:
            delivered_time (int): The time when his last order is delivered
            delivery_time (int): The time he spend on his way back to the restaurant
        """
        self.arrived_time = delivered_time + delivery_time
