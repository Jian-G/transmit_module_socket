import paddle
import glob
import numpy as np

def edge_load_model(path_prefix):
    paddle.enable_static()

    startup_prog = paddle.static.default_startup_program()


    exe = paddle.static.Executor(paddle.CPUPlace())
    exe.run(startup_prog)

    # 保存预测模型

    [inference_program, feed_target_names, fetch_targets] = (
        paddle.static.load_inference_model(path_prefix, exe))
    tensor_img = np.array(np.random.random((1, 3, 32, 32)), dtype=np.float32)
    results = exe.run(inference_program,
              feed={feed_target_names[0]: tensor_img},
              fetch_list=fetch_targets)
    
    return np.array(results[0])

def cloud_load_tensor(path_prefix, tensor):
    paddle.enable_static()
    startup_prog = paddle.static.default_startup_program()


    exe = paddle.static.Executor(paddle.CPUPlace())
    exe.run(startup_prog)

    # 保存预测模型

    [inference_program, feed_target_names, fetch_targets] = (
        paddle.static.load_inference_model(path_prefix, exe))

    results = exe.run(inference_program,
              feed={feed_target_names[0]: tensor},
              fetch_list=fetch_targets)
    results = results[0].tolist()
    return [result[i].index(max(result[i])) for i in range(len(result))]

if __name__ == "__main__":
    for filename in glob.glob(r'data/send/model/client_*_infer.pdmodel'):
        print(filename)

    tensor = edge_load_model()
    result = cloud_load_tensor(tensor)[0].tolist()
    print([result[i].index(max(result[i])) for i in range(len(result))])






