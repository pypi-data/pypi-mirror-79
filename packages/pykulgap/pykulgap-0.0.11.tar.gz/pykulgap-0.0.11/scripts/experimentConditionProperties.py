## ---- Defining object attributes to get and set attributes, allows type checking and other error handling
@property
def name(self):
    try:
        return self.__name
    except "Accessing name attribute failed, is it defined?" as e:
        raise AttributeError(e)


@name.setter
def name(self, new_name):
    if isinstance(new_name, str):
        self.__name = new_name
    else:
        raise AttributeError("The name attribute must be a string!")


@property
def variable(self):
    try:
        return self.__variable
    except "Accessing name attribute failed, is it defined?" as e:
        raise AttributeError(e)


@variable.setter
def variable(self, new_variable):
    if isinstance(new_variable, np.array):
        if isinstance(new_variable.flat[0], np.float) or isinstance(new_variable.flat[0], np.int):
            self.__variable = new_variable
        else:
            raise ValueError("The variable attribute of an ExperimentalCondition must be an numpy array of"
                             "type float or int!")
    else:
        raise ValueError("The variable attribute must be a numpy array!")


@property
def response(self):
    try:
        return self.__response
    except "Accessing response attribute failed, is it defined?" as e:
        raise AttributeError(e)


# @response.setter
# def response(self, new_response):
#     if _is_numpy_float_or_int_array(new_response):
#         self.__response = new_response


@property
def response_norm(self):
    try:
        return self.__response_norm
    except AttributeError:
        print("The response_norm attribute is not populated, calculating it now...")
        self.response_norm = self.response / self.response[0]
        return self.__response_norm


@response_norm.setter
def response_norm(self, new_response_norm):
    if new_response_norm is None:
        self.__response_norm = new_response_norm
    elif isinstance(new_response_norm, np.array):
        if isinstance(new_response_norm, np.float) or isinstance(new_response_norm, np.int):
            self.__response_norm = new_response_norm
        else:
            raise AttributeError("The response_norm_attribute must be None or a numpy array of type float or int")
    else:
        raise AttributeError("The response attribute must be a numpy array!")


@property
def