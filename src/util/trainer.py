import tensorflow as tf
import time


def train_model(model, train_step, loss_fcn,
                train_dataset, eval_dataset, processed,
                optimizer, iterations, batch_size, save_checkpoint_steps, save_checkpoint_path,
                eval_batch_size, eval_steps):
    train_dataset = train_dataset.batch(batch_size).repeat()
    eval_dataset = eval_dataset.batch(eval_batch_size).repeat(1)

    for iter, train_batch in enumerate(train_dataset):
        if iter > iterations:
            break

        train_loss = train_step(model, train_batch, optimizer)

        if iter % save_checkpoint_steps == 0:
            print("Iter: {}/{} - Checkpoint reached. Saving the model...".format(iter, iterations))
            model.save_weights(save_checkpoint_path + "_iter_{}".format(iter))

        if iter % eval_steps == 0:
            loss_mean = tf.keras.metrics.Mean()
            for eval_batch in eval_dataset:
                loss_mean(loss_fcn(model, eval_batch))

            end = time.time()

            print("Iter: {}/{} - Train loss: {}, Eval loss: {}, Time: {}".
                  format(iter, iterations, train_loss, loss_mean.result(), 0 if iter == 0 else end-start))

            start = time.time()
