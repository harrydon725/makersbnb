from datetime import datetime


class Space():

    def __init__(self, id, title, price, start_date, end_date, ownerid):
        self.id = id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.ownerid = ownerid
        self.price = price


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space({self.id}, {str(self.title)}, {self.start_date}, {self.end_date}, {self.ownerid}, {self.price})"

    def generate_errors(self):
        errors = []
        if self.title == None or self.title == "":
            errors.append("Title can't be blank")
        if self.price == None or self.price == "":
            errors.append("Price can't be blank")
        if not isinstance(self.price, int):
            if not isinstance(self.price, float):
                errors.append("Price has to be a number (up to 2 decimals)")
        if self.start_date == None or self.start_date == "":
            errors.append("Start date can't be blank")
        if self.end_date == None or self.end_date == "":
            errors.append("End date can't be blank")
        # Space for description validation
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)

    def is_valid(self):
        if self.title == None or self.title == "":
            return False
        elif self.price == None or self.price == "":
            return False
        elif not isinstance(self.price, int):
            if not isinstance(self.price, float):
                return False
        elif self.start_date == None or self.start_date == "":
            return False
        elif self.end_date == None or self.end_date == "":
            return False
            # Space for description validation
        return True
