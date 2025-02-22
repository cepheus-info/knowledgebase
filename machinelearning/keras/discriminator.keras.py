from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Reshape, Lambda
from tensorflow.keras.models import Model
import tensorflow as tf

def ProjectionLayer(embedding_dim):
    def project(inputs):
        x, emb = inputs
        # Assuming x shape is (batch, height, width, channels) and emb is (batch, embedding_dim)
        # Adjust dimensions for broadcasting
        emb = tf.reshape(emb, (-1, 1, 1, embedding_dim))
        # Project and sum across embedding dimension
        projected = tf.reduce_sum(x * emb, axis=-1, keepdims=True)
        return projected
    return Lambda(project)

def build_discriminator(img_shape, n_fonts, n_chars, embedding_dim):
    inputs = Input(shape=img_shape)
    font_input = Input(shape=(1,), dtype='int32')
    char_input = Input(shape=(1,), dtype='int32')

    # Embeddings
    font_embedding = Embedding(n_fonts, embedding_dim)(font_input)
    char_embedding = Embedding(n_chars, embedding_dim)(char_input)

    # Flatten embeddings
    font_embedding = Flatten()(font_embedding)
    char_embedding = Flatten()(char_embedding)

    # Projection
    font_projected = ProjectionLayer(embedding_dim)([inputs, font_embedding])
    char_projected = ProjectionLayer(embedding_dim)([inputs, char_embedding])

    # Combine and process
    combined = tf.concat([font_projected, char_projected], axis=-1)
    combined = Flatten()(combined)
    x = Dense(512, activation='relu')(combined)
    x = Dense(1, activation='sigmoid')(x)

    model = Model([inputs, font_input, char_input], x)
    return model