from Picture import ImageConcretion
import random


class Model3DMutater:
    def __init__(self, file_picture_manager, models_3D, model_3D_adaption, address):
        self.mutation_address = address
        self.MA = model_3D_adaption
        self.IC = ImageConcretion()
        self.FP = file_picture_manager
        self.Models_3D = models_3D


    def mutate_models(self, picture_addresses):
        zoom_range = 1
        xyz_ranges = {'x': 1, 'y': 1, 'z':20}
        start_position = [5, 5, 10]

        mutated_model_addresses = []
        for model_count, picture_address in enumerate(picture_addresses):
            model_nr = self.MA.get_model_nr_from_picture_address(picture_address)

            pre_model = self.Models_3D.get_pre_models_3d(model_nr)
            mutated_pre_model  = self._mutate_pre_model(pre_model)

            mutated_model = self.Models_3D._transform_pre_model_to_model(mutated_pre_model)
            rotated_mutated_models = self.MA.generate_model_rotations(mutated_model, zoom_range, xyz_ranges, start_position)

            mutated_model_addresses = mutated_model_addresses + self._save_mutations(rotated_mutated_models, model_count)
        return mutated_model_addresses


    def _save_mutations(self, rotated_models, model_count):
        addresses = []
        for rotation_count, rotated_model in enumerate(rotated_models):
            mutated_model_concretion = self.IC.make_snapshot_of_model(rotated_model)
            mutated_model_image      = self.IC.convert_snapshot_to_image(mutated_model_concretion)

            name = "Mutation" + str(model_count) + "_Rotation" + str(rotation_count) + ".PNG"
            addresses.append(self.mutation_address + name)

            self.FP.save_picture(mutated_model_image, self.mutation_address, name)

        return addresses

    def _mutate_pre_model(self, model):
        vectors = model[3]
        for vectorCounter, vector in enumerate(vectors):
            for elementCounter, element in enumerate(vector):
                if int(element) > 1:
                    if random.randint(0,3) == 2:
                        model[3][vectorCounter][elementCounter] = str(round(int(model[3][vectorCounter][elementCounter])/2))
        return model
