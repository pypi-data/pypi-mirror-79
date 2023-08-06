import matplotlib.pyplot as plt # plotting
import os # for file/folder creations
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# =======================================================================================
# BEG: build custom model based on args
# =======================================================================================
class TestModel:
    def __init__(self, args):
        # build model
        self.model = self.build_model(args)    
    
    def build_model(self, args):
        # define input dims
        input_dims = Input(shape=args.input_shape)#(32,32,3)) # flexible batch size
        
        x = self.convs_from_seq(args.conv_seq, input_dims)
        x = Flatten()(x)
        x = self.fcs_from_seq(args.fcs_seq, x)
        
        return Model(inputs=input_dims, outputs=x)
    
    def compile(self, args):
        # configure optimizer
        # rmsprop
        if args.optimizer == 'RMSprop':
            opt = keras.optimizers.RMSprop(
                lr     = args.lr, 
                decay  = args.rms_decay
            )
        elif args.optimizer == 'SGD':
            opt = keras.optimizers.SGD(
                learning_rate  = args.lr, 
                momentum       = args.sgd_momentum, 
                nesterov       = args.sgd_nesterov, 
            )

        # Create our model by compiling
        self.model.compile(
            loss       = args.loss,
            optimizer  = opt,
            metrics    = args.metrics,
        )
    
    # ----------------------------------------------------------
    # Training and evaluation
    # ----------------------------------------------------------
    def fit(self, train_data, val_data, v, args):
        """train_data, val_data are tuples of X and y"""
        if v==0:
            print("Wait for the big picture ☕️\n\nTrainng started ...")
        num_samples = train_data[0].shape[0] #X
        num_batches = num_samples / args.batch_size
        
        callbacks_list = []
        if 'CustomCallback' in args.__dict__:
            callbacks_list.append(args.CustomCallback(num_batches))
        
        self.history = self.model.fit(
            train_data[0], #X
            train_data[1], #y
            validation_data = val_data,
            batch_size      = args.batch_size,
            epochs          = args.epochs,
            shuffle         = args.shuffle,
            verbose         = v,
            callbacks       = callbacks_list
            
        )
    
    # evaluation
    def evaluate(self, x_test, y_test, v=1):
        print("Evaluating on test data...\n")
        test_loss, test_acc = \
            self.model.evaluate(x_test, y_test, verbose=v)
        print(f"+ Test Loss\t:{test_loss}\n+ Test Acc\t:{test_acc}")
    
    # save
    def save_to(self, save_dir):
        self.model.save(save_dir)
    
    # -----------------------------------------------------------
    # plot
    # -----------------------------------------------------------
    def plot(self):
        history_dict = self.history.history
        
        # Plot loss chart
        loss_values     = history_dict['loss']
        val_loss_values = history_dict['val_loss']
        epochs          = range(1, len(loss_values) + 1)
        
        line1 = plt.plot(epochs, val_loss_values, label='Validation/Test Loss')
        line2 = plt.plot(epochs, loss_values, label='Training Loss')
        
        plt.setp(line1, linewidth=2.0, marker = '+', markersize=10.0)
        plt.setp(line2, linewidth=2.0, marker = '4', markersize=10.0)
        plt.xlabel('Epochs') 
        plt.ylabel('Loss')
        plt.grid(True)
        plt.legend()
        
        # Plot acc chart
        acc_values      = history_dict['accuracy']
        val_acc_values  = history_dict['val_accuracy']
        epochs          = range(1, len(loss_values) + 1)

        line1 = plt.plot(epochs, val_acc_values, label='Validation/Test Accuracy')
        line2 = plt.plot(epochs, acc_values, label='Training Accuracy')
        
        plt.setp(line1, linewidth=2.0, marker = '+', markersize=10.0)
        plt.setp(line2, linewidth=2.0, marker = '4', markersize=10.0)
        plt.xlabel('Epochs') 
        plt.ylabel('Accuracy')
        plt.grid(True)
        plt.legend()        
        
        # display
        plt.show()
    
    def summary(self):
        keras.utils.plot_model(
            self.model,
            to_file="model.png",
            show_shapes=False,
            #show_dtype=False,
            show_layer_names=True,
            rankdir="TB",
            expand_nested=False,
            dpi=96,
        )
        return self.model.summary()    
    # ===========================================================
    # BEG: build_model helpers
    # ===========================================================
    def convs_from_seq(self, seq, x):
        """
        + x is input which will be forwarded in series 
        + seq is of format
            [
                {"out_ch": int, "z": int, 'act': 'relu'},
                {"out_ch": int, "z": int, 'act': 'relu', "maxpool_z": 2},
                # -------------------------------------------------------
                {"out_ch": int, "z": int, 'act': 'relu'},
                ....
            ]
        """
        # bulid series
        series = []
        for config in seq:
            # append convs and nonlin one-by-one
            series.append(
                self.__get_conv(
                    out_ch   = config['out_ch'],
                    z        = config['z'],
                    padding  = 'same'
                )
            )
            # activation function
            series.append(self.__get_act(config['act']))
            # pool if specified
            if 'maxpool_z' in config.keys():
                # append pool one-by-one
                series.append(self.__get_pool(config['maxpool_z']))
        
        # forward through series
        """ #OVERKILL
        return Sequential(series)
        """
        for layer in series:
            x = layer(x)
        return x

    def fcs_from_seq(self, seq, x):
        """
        + x is input
        + seq is of format
            [
                {"out_nodes": int, "act": 'relu', 'p': 0   },
                {"out_nodes": int, "act": 'relu', 'p': 0.5 },
                ....
            ]
        """
        # build series
        series = []
        for config in seq:
            series.append(
                self.__get_dense(
                    out_nodes  = config["out_nodes"], 
                    act        = config["act"]
                )
            )
            # dropout
            series.append(self.__get_dropout(config["p"]))
        
        # forward through series
        """ # OVERKILL
        return Sequential(series)
        """
        for layer in series:
            x = layer(x)
        return x

        
    # helpers start ---------------------------------
    # general
    def __get_act(self, name):
        """`name` is a string. eg. 'relu'"""
        return Activation(name)
    
    # for convs_seq
    def __get_conv(self, out_ch, z, padding):
        """
        For "SAME" padding, if you use a stride of 1, the layer's outputs will have the same spatial dimensions as its inputs.
        """
        return Conv2D(out_ch, (z, z), padding=padding, strides=(1, 1))
    
    def __get_pool(self, z):
        return MaxPooling2D(pool_size=(z, z))
    
    # for fcs_Seq
    def __get_dense(self, out_nodes, act):
        """out_nodes is int and act is string """
        return Dense(out_nodes, activation=act)
    
    def __get_dropout(self, p):
        """ p if float [0, 1]"""
        return Dropout(p)
    # helpers end ------------------------------------
    # ===========================================================
    # END: build_model helpers 
    # ===========================================================
# =======================================================================================
# END: build custom model based on args
# =======================================================================================