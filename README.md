# Getting Started
## Running DaCo
### Preparation: table&KG
>In Class_Table.py, we have implemented a table class. Users can store their tables in the format of this class and place the folder in the "daco" directory to run the program. The path to read the table data is recorded in the function "read_data_sample" in the file "read_data.py," where the variable "infile" represents the path to the table file. 
>
>Additionally, we have established an index for the DBpedia files, and the indexed knowledge graph can be downloaded from the provided link: (https://pan.baidu.com/s/1i6F_IlwwduJWwZ49sRyAJg? pwd=8888). Please ensure to place the downloaded knowledge graph files in the "index KG" folder, for example, by placing the "triple" folder inside the "index KG" directory.
### Executing
>You can run this algorithm by executing the "Iteration_norm.py".
### Example
> 1. Download the "t2d_example" folder from the provided link (https://pan.baidu.com/s/1ARbWAdDGxHNzaHGjq92z-g?pwd=8888).
> 
> 2. Place the downloaded "t2d_example" folder inside the "daco" folder in your local directory.
>
> 3. Ensure that you have the required Python environment, rdflib 6.0.0 and networkx 1.11 installed to run the DaCo algorithm.
>
>4. After running the script, the results will be stored in the "text_result" folder. Each table's core columns will be saved in files with names like "table_name+cc.data".
