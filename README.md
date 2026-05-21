# HerbOS


## Install
```bash
# create python virtual environment for the project
pythom -m venv .venv

# activate the virtual environment
# windows:
.venv/Scripts/activate
# linux:
.venv/bin/activate

# install project dependencies
pip install -r requirements.txt
```

## Run
```bash
python app.py 
```

## Lerobot skills
```bash
# install dependencies
pip install lerobot
pip install imageio-ffmpeg
pip install lerobot[feetech]

# 查询端口号
lerobot-find-port

# 标定限位
lerobot-calibrate --robot.type=so101_follower --robot.port=COM6 --robot.id=my_awesome_follower_arm
lerobot-calibrate --teleop.type=so101_leader --teleop.port=COM5 --teleop.id=my_awesome_leader_arm

# 启动遥操
lerobot-teleoperate --robot.type=so101_follower --robot.port=COM6 --robot.id=my_awesome_follower_arm --teleop.type=so101_leader --teleop.port=COM5 --teleop.id=my_awesome_leader_arm

# 查询可用的摄像头
lerobot-find-cameras opencv

# 登录hugging face
set HUGGINGFACE_TOKEN [登录huggingface后，通过个人信息获得]
set HF_USER [替换为你的名字]
hf auth login --token $HUGGINGFACE_TOKEN --add-to-git-credential

# 采集数据
lerobot-record `
    --robot.type=so101_follower `
    --robot.port=COM6 `
    --robot.id=my_awesome_follower_arm `
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 15}}" `
    --teleop.type=so101_leader `
    --teleop.port=COM5 `
    --teleop.id=my_awesome_leader_arm `
    --display_data=true `
    --dataset.repo_id=${HF_USER}/record-test `
    --dataset.num_episodes=100 `
    --dataset.single_task="Classify the red things and white things" `
    --dataset.streaming_encoding=true `
    --dataset.encoder_threads=2 `
    --dataset.push_to_hub=False
    # --dataset.vcodec=auto `

# 训练ACT模型
lerobot-train `
  --dataset.repo_id=${HF_USER}/record-test `
  --policy.type=act `
  --output_dir=datasets/train/act_record_test `
  --job_name=act_record-test `
  --policy.device=cuda `
  --wandb.enable=true `
  --policy.repo_id=${HF_USER}/act_policy


# 执行训练好的模型（此步仍在验证中）
lerobot-record  `
  --robot.type=so101_follower `
  --robot.port=COM6 `
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 15}}" `
  --robot.id=my_awesome_follower_arm `
  --display_data=false `
  --dataset.repo_id=liu-ruibin/eval_so100 `
  --dataset.single_task="Classify the red things and white things" `
  --dataset.streaming_encoding=true `
  --dataset.encoder_threads=2 `
  --policy.path=C:\Users\ruibi\.cache\huggingface\lerobot\liu-ruibin/pretrained_model
  # --dataset.vcodec=auto `
  # <- Teleop optional if you want to teleoperate in between episodes `
  # --teleop.type=so100_leader `
  # --teleop.port=/dev/ttyACM0 `
  # --teleop.id=my_awesome_leader_arm `
```