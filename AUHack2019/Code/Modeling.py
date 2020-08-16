import os
import copy
import math
import numpy as np
from Picture import ImageConcretion

from MatrixCalculations import MatrixCalculations



class ModelAdaption:
    def __init__(self, file_picture_manager, models_3D, snapshot_address):
        self.FP = file_picture_manager
        self.MC = MatrixCalculations()
        self.IC = ImageConcretion()

        self.rotated_models = self._generate_models_rotations(models_3D)
        self.rotated_models_snapshot_addresses = self._save_snapshot_of_rotations(self.rotated_models, snapshot_address)


    def get_snapshot_addresses(self):
        return self.rotated_models_snapshot_addresses

    def get_model_nr_from_picture_address(self, picture_address):
        address_index = self.rotated_models_snapshot_addresses.index(picture_address)
        model_nr = math.floor(float(address_index) / float(20))
        return model_nr


    def _generate_models_rotations(self, models_3D):
        #Return a list of all rotatiosn of the matrix
        model_rotations_list = []
        zoom_range = 1
        xyz_ranges = {'x': 1, 'y': 1, 'z':20}

        start_position = [5, 5, 10]
        for model_3D in models_3D.get_models_3d():
            model_rotations = self.generate_model_rotations(model_3D, zoom_range, xyz_ranges, start_position)
            model_rotations_list.append(model_rotations)

        return model_rotations_list


    def generate_model_rotations(self, model_3D, zoom_range, xyz_ranges, start_position):
        model_rotations = []

        for zoom in range(1, zoom_range+1):
            for x_range in range(0, xyz_ranges['x']):
                for y_range in range(0, xyz_ranges['y']):
                    for z_range in range(0, xyz_ranges['z']):
                        rotated_d_model = self._get_rotation(model_3D, zoom, start_position, x_range, y_range, z_range)
                        model_rotations.append([rotated_d_model, model_3D[3]])

        return model_rotations


    def _get_rotation(self, model_3D, zoom, start_position, x_range, y_range, z_range):
        zero_matrix = self.MC.generate_zero_matrix(len(model_3D[2]), len(model_3D[2]))

        P   = self._get_P_rotation(copy.deepcopy(zero_matrix), zoom, start_position)
        P_X = self._get_PX_rotation(copy.deepcopy(zero_matrix), (x_range/10))
        P_Y = self._get_PY_rotation(copy.deepcopy(zero_matrix), (y_range/10))
        P_Z = self._get_PZ_rotation(copy.deepcopy(zero_matrix), (z_range/10))

        rotated_matrix = self.MC.multiply_matrices(P, P_Z)
        rotated_matrix = self.MC.multiply_matrices(rotated_matrix, model_3D[2])

        for columnCounter, column in enumerate(model_3D[2][0]):
            #Divide row 1 with row 4
            rotated_matrix[0][columnCounter] = float(rotated_matrix[0][columnCounter]) / float(rotated_matrix[3][columnCounter])
            #Divide row 2 with row 4
            rotated_matrix[1][columnCounter] = float(rotated_matrix[1][columnCounter]) / float(rotated_matrix[3][columnCounter])

        D2Matrix = self.MC.generate_zero_matrix(len(model_3D[2][0]),2)
        for rowCounter, rowElement in enumerate(D2Matrix):
            D2Matrix[rowCounter][0] = rotated_matrix[0][rowCounter]
            D2Matrix[rowCounter][1] = rotated_matrix[1][rowCounter]

        return D2Matrix


    def _get_P_rotation(self, zero_matrix, zoom, start_position):
        zero_matrix[0][0] = zoom
        zero_matrix[0][2] = -((start_position[0])/(start_position[2]))

        zero_matrix[1][1] = zoom
        zero_matrix[1][2] = -((start_position[1])/(start_position[2]))

        zero_matrix[2][2] = zoom

        zero_matrix[3][2] = -(1/(start_position[2]))
        zero_matrix[3][3] = 1
        return zero_matrix


    def _get_PX_rotation(self, zero_matrix, x_rotation):
        zero_matrix[0][0] = 1

        zero_matrix[1][1] = math.cos(x_rotation)
        zero_matrix[1][2] = -math.sin(x_rotation)

        zero_matrix[2][1] = math.sin(x_rotation)
        zero_matrix[2][2] = math.cos(x_rotation)

        zero_matrix[3][3] = 1
        return zero_matrix


    def _get_PY_rotation(self, zero_matrix, y_rotation):
        zero_matrix[0][0] = math.cos(y_rotation)
        zero_matrix[0][2] = math.sin(y_rotation)

        zero_matrix[1][1] = 1

        zero_matrix[2][0] = -math.sin(y_rotation)
        zero_matrix[2][2] = math.cos(y_rotation)

        zero_matrix[3][3] = 1
        return zero_matrix


    def _get_PZ_rotation(self, zero_matrix, z_rotation):
        zero_matrix[0][0] = math.cos(z_rotation)
        zero_matrix[0][1] = -math.sin(z_rotation)

        zero_matrix[1][0] = math.sin(z_rotation)
        zero_matrix[1][1] = math.cos(z_rotation)

        zero_matrix[2][2] = 1

        zero_matrix[3][3] = 1
        return zero_matrix


    def _save_snapshot_of_rotations(self, models_rotations, snapshot_address):
        snapshot_addresses = []
        for model_count, model_rotations in enumerate(models_rotations):
            for rotation_count, model_rotation in enumerate(model_rotations):
                snapshot_array = self.IC.make_snapshot_of_model(model_rotation)
                snapshot_img   = self.IC.convert_snapshot_to_image(snapshot_array)

                name = "Model" + str(model_count) + "_Rotation" + str(rotation_count) + ".PNG"
                snapshot_addresses.append(snapshot_address + name)

                self.FP.save_picture(snapshot_img, snapshot_address, name)
        return snapshot_addresses








class Modeling3D:
    def __init__(self, models_3d_address):
        self.models_3D_address = models_3d_address
        self.MC = MatrixCalculations()
        self.models_3D = self._load_3d_models()


    def get_models_3d(self):
        return self.models_3D


    def get_pre_models_3d(self, model_nr):
        files = self._get_all_model_addresses(self.models_3D_address)
        with open(files[model_nr], 'r') as model_file:
            return self._transform_string_to_pre_model(model_file)


    def _load_3d_models(self):
        files = self._get_all_model_addresses(self.models_3D_address)

        model_3D_list = []

        for file_address in files:
            with open(file_address, 'r') as model_file:
                pre_model_3D = self._transform_string_to_pre_model(model_file)
                model_3D = self._transform_pre_model_to_model(pre_model_3D)
                model_3D_list.append(model_3D)

        return model_3D_list


    def _get_all_model_addresses(self, models_3d_address):
        for root, dir, files in os.walk(models_3d_address):
            file_list = [os.path.join(root, file) for file in files if '.txt' in file]
        return file_list


    def _transform_string_to_pre_model(self, model_file):
        text_buffer = [row.rstrip() for row in model_file]

        pre_model = []
        pre_model.append(self._get_model_id(text_buffer))
        pre_model.append(self._get_model_rules(text_buffer))
        pre_model.append(self._get_model_connections(text_buffer))
        pre_model.append(self._get_model_vectors(text_buffer))

        return pre_model


    def _get_model_id(self, file_content):
        return file_content[0]


    def _get_model_rules(self, file_content):
        rule_length = len("Rules: ")
        rules = file_content[1][rule_length:].split(",")
        return rules


    def _get_model_connections(self, file_content):
        connection_length = len("Connections: ")
        connections = file_content[2][connection_length:].split(",")
        return connections


    def _get_model_vectors(self, file_content):
        vectors = [row.split(',') for row in file_content[3:]]
        return vectors


    def _transform_pre_model_to_model(self, pre_model):
        number_of_vectors = len(pre_model[3])

        zero_matrix_d = self.MC.generate_zero_matrix(4, number_of_vectors)
        zero_matrix_c = self.MC.generate_zero_matrix(number_of_vectors, number_of_vectors)

        d_matrix = self._generate_d_matrix(pre_model[3], zero_matrix_d)
        c_matrix = self._insert_connections(pre_model[2], zero_matrix_c)

        return [pre_model[0], pre_model[1], d_matrix, c_matrix]


    def _generate_d_matrix(self, vectors, d_matrix):
        for col_nr, vector in enumerate(vectors):
            for row_nr, element in enumerate(vector):
                d_matrix[row_nr][col_nr] = element
            d_matrix[-1][col_nr] = 1

        return d_matrix


    def _insert_connections(self, connections, zero_matrix):
        for connection_segment in connections:
            [connection_from, connections_to] = connection_segment.split(":")

            for connection in connections_to.split("-"):
                row_nr = int(connection_from)
                col_nr = int(connection)
                zero_matrix[row_nr-1][col_nr-1] = 1

        return zero_matrix






#Nothing
