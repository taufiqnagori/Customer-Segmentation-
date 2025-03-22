from tkinter import *
from tkinter import filedialog
import pandas as pd
import os
from tkinter import messagebox
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
import warnings

import matplotlib.pyplot as plt

window = Tk()
window.title("Customer Segmentation")
window.geometry("1280x720")
window.config(bg="#000",pady=20,padx=20)

def load_file():
    global browse_file, data, features_entry
    file_path = filedialog.askopenfilename(filetypes=[("CSV File","*.csv")])
    try:
        data = pd.read_csv(file_path,encoding="ISO-8859-1")
        file_name = os.path.basename(file_path)
        browse_file.config(text=file_name)
        data_frame = pd.DataFrame(data)
        data_columns = ",".join(data_frame.columns)
        features_entry_var.set(data_columns)
        features_entry.update()
        
    except FileNotFoundError:
        messagebox.showerror("Error","File Not Found. Please Select a valid CSV File.")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error","File is Empty. Please Select a valid CSV File.")
    except pd.errors.ParseError:
        messagebox.showerror("Error","Error Parsing File. Please Select a valid CSV File.")
        
def segment_customer():
    global data, kmeans
    if data is None:
        messagebox.showerror("Error","Plese load CSV file first.")
        return
    features_entry_list = features_entry_var.get().split(",")
    X = data[features_entry_list]
    try:
        num_clusters = int(cluster_entry_var.get())
    except ValueError:
        print("Invalid number of Clusters. Please enter an Integer")
        messagebox.showerror("Error","Invalid number of Clusters. Please enter an Integer")
        return
    kmeans = KMeans(n_clusters=num_clusters,n_init=10)
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',category=ConvergenceWarning())
        kmeans.fit(X)
    labels = kmeans.labels_
    num_features = len(features_entry_list)
    if num_features <=3:
        plot_func = globals()[f"plot_{num_features}d"]
        plot_func(X, labels, features_entry_list)
    else:
       plot_nd_message("Cannot Visualize higher than 3D. Consider reducing features or using PCA")

def plot_2d(X, labels, features):
    plt.figure(figsize=(8,6))
    plt.scatter(X.iloc[:,0],X.iloc[:,1],c=labels,cmap="viridis",label="Clusters")
    plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],marker="x",color="red",label="Centroids")
    plt.xlabel(features[0])
    plt.ylabel(features[1])
    plt.title("Customer Segmentation")
    plt.legend()
    plt.show()  

def plot_3d(X, labels, features):
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111,projection="3d")
    ax.scatter(X.iloc[:,0],X.iloc[:,1],X.iloc[:,2],c=labels,cmap="viridis", label="Clusters")
    ax.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],kmeans.cluster_centers_[:,2],marker="x",color="red",label="Centroids")
    ax.set_xlabel(features[0])
    ax.set_ylabel(features[1])
    ax.set_zlabel(features[2])
    ax.set_title("Customer Segmentation")
    ax.legend()
    plt.show()

def plot_nd_message(message):
    plt.figure(figsize=(8,6))
    plt.text(0.5,0.5,message,ha="center",va="center",fontsize=12)
    plt.axis("off")
    plt.show()
    
frame= Frame(window, bg='#ff4508', relief=SUNKEN, highlightthickness=5, highlightbackground='#4f4e4d')
frame.pack(fill=BOTH, expand=True)

heading = Label(frame, text="Customer Segmentation : ", font="Arial 30 bold", bg="#f7a98f", padx=30, fg="black")
heading.pack(pady=10)

frame2 = Frame(frame, bg="#ff4508", highlightthickness=5, highlightbackground="#f7a98f", padx=30, highlightcolor="#f7a98f")
frame2.pack(pady=20)

select_csv = Label(frame2, text="Select CSV File : ", font="Arial 20 bold", bg="#ff4508")
select_csv.grid(row=2, column=0, pady=10, padx=10)

browse_file= Button(frame2, text= "Select CSV File", font="Arial 14 bold", bg="#f7a98f", command=load_file)
browse_file.grid(row=2, column=1, pady=10, padx=10)

features_label = Label(frame2, text="Select Features for Clustering : ", font="Arial 20 bold", bg="#ff4508")
features_label.grid(row=3, column=0, pady=10, padx=10)
features_entry_var = StringVar()

features_entry = Entry(frame2, textvariable=features_entry_var, width=30, font="Arial 14 bold",bg="#f7a98f")
features_entry.grid(row=3, column=1, pady=10, padx=10)

cluster_label = Label(frame2, text="Number of Clusters : ", font="Arial 20 bold", bg="#ff4508")
cluster_label.grid(row=4, column=0, pady=10, padx=10)
cluster_entry_var = StringVar()
cluster_entry = Entry(frame2, textvariable=cluster_entry_var, width=30, font="Arial 14 bold",bg="#f7a98f")
cluster_entry.grid(row=4, column=1, pady=10, padx=10)

segment_button= Button(frame2, text= "Segment Clusters", font="Arial 14 bold", bg="#f7a98f", command=segment_customer)
segment_button.grid(row=5, column=0, columnspan=2, pady=10)

window.mainloop()
