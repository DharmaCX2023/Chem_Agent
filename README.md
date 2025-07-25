# AI Chemistry Research Assistant (Powered by GPT-4o)

## What it can do? 
1. Find properties of chemicals by coordinating multiple APIs. 
2. Find relevant patents from Google Patents.
3. Web search is integrated to find chemistry-related information about chemicals. 

## User Guidance

### Step 1: Install Dependencies
Run the following command to install required packages:
```bash
conda create -n my_env
conda install -c conda-forge rdkit
pip install -r requirements.txt
```
### Step 2: Use the assistant
Run the AI research assistant:
```bash
streamlit run main.py
```
Enter your OpenAI and Serpapi tokens in the sidebar and start chatting!

## Credits
- *Created by: Xi Chen,* *Email: chenxi17@tsinghua.org.cn*