Step 1: "Unzip" the tar file via running the command tar xzvf coursework1.tar.gz
Step 2: Replace the "test.csv" that exists inside the 'data' folder with your test dataset and keep the same naming convention.
Step 3: Run the following command to create the docker image: docker build -t coursework1 . 
Step 4: Run the container based on the image created at Step 3, i.e. run the command: docker run -v ./data:/data coursework1:latest