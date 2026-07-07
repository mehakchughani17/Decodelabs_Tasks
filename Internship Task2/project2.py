# Step 1: Import Libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Step 2: Load Dataset
iris = load_iris()
A = iris.data   # features
B = iris.target # labels

# Step 3: Split Data
A_train, A_test, B_train, B_test = train_test_split(
    A, B, test_size=0.2, random_state=22
)

# Step 4: Ask User for Algorithm Choice
print("Choose an algorithm:")
print("1 - Decision Tree")
print("2 - KNN (k=5)")
choice = input("Enter 1 or 2: ")

# Step 5: Train & Evaluate based on choice
if choice == "1":
    print("\n=== Decision Tree Classifier ===")
    model = DecisionTreeClassifier()
elif choice == "2":
    print("\n=== KNN Classifier (k=5) ===")
    model = KNeighborsClassifier(n_neighbors=5)
else:
    print("Invalid choice! Defaulting to Decision Tree.")
    model = DecisionTreeClassifier()

# Train the chosen model
model.fit(A_train, B_train)
B_pred = model.predict(A_test)

# Step 6: Evaluation
print("Confusion Matrix:\n", confusion_matrix(B_test, B_pred))
print("\nClassification Report:\n", classification_report(B_test, B_pred))
