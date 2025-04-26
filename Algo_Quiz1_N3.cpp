#include <iostream>
#include <vector>
using namespace std;

const int inf = 2e9;

struct node {
    node* parent;
    node* l;
    node* r;
    int val;

    node(node* par) : parent(par), l(nullptr), r(nullptr), val(inf) {}
    node() : parent(nullptr), l(nullptr), r(nullptr), val(inf) {}
};

struct tree {
    //vector<int> arr; // используется ТОЛЬКО для инициализации дерева
    node* main_root; // Изменен на указатель для удобства
    int cur_size = 0;

    // Создает поддерево
    node* create_subtree(node* par, int Li, int Ri, const vector <int> &arr) {
        if (Li > Ri) return nullptr; // Проверка на правильные границы

        node* root = new node(par);
        root->val = arr[(Ri + Li) / 2]; // устанавливаем значение корня

        // Создание левого и правого поддеревьев
        root->l = create_subtree(root, Li, (Ri + Li) / 2 - 1, arr);
        root->r = create_subtree(root, (Ri + Li) / 2 + 1, Ri, arr);

        return root; // Возвращаем указатель на созданный узел
    }

    // Инициализация дерева
    void create(const vector <int> &arr) {
        cur_size = arr.size();
        if (arr.size() == 0) {
            main_root = nullptr; // В случае пустого массива
        } else {
            main_root = create_subtree(nullptr, 0, arr.size() - 1, arr);
        }
        cout << "Tree created\n";
    }

    // Обход дерева (in-order)
    void trav(node* root) {
        if (root == nullptr) return; // Проверка на nullptr
        trav(root->l); // Обход левого поддерева
        cout << root->val << " "; // Обработка текущего узла
        trav(root->r); // Обход правого поддерева
    }

    void replace_el(node* root, int Li, int Ri, int i, int x) {
        if (root == nullptr) return;

        int mid = (Li + Ri) / 2;
        if (i == mid) {  // Нашли узел, который нужно заменить
            root->val = x;
            return;
        }

        if (i < mid) {
            replace_el(root->l, Li, mid - 1, i, x);  // Ищем в левом поддереве
        } else {
            replace_el(root->r, mid + 1, Ri, i, x);  // Ищем в правом поддереве
        }
    }

    void del(node* &root) {
        if (root == nullptr) {
            return;
        }
        del(root->l);
        del(root->r);
        if (root->l == nullptr && root->r == nullptr) {
            cout << "clidren already nullptr\n";
        }
        cout << "del:" << root->val << "\n";
        delete root;
        root = nullptr;
        if (root == nullptr) {
            cout << "successfully deleted\n";
            cout << "\n";
        }
    }

    int sum_subtree(node* &root) {
        if (root == nullptr) {
            return 0;
        }
        if (root->l == nullptr && root->r == nullptr) {
            int res = root->val;
            root->val = 0;
            return res;
        }
        int L = sum_subtree(root->l);
        int R = sum_subtree(root->r);
        int old_val = root->val;
        root->val = L + R;
        if (root == main_root) {
            root->val += old_val;
        }
        return  old_val + L + R;
    }
};

bool cmp(node* root1, node* root2) {
     if  (root1 == nullptr) {
        if (root2 != nullptr) {
            return 0;
        }
        return 1;
     }  else if(root2 == nullptr){
         if (root1 != nullptr) {
            return 0;
         }
         return 1;
     }
     if (root1->val != root2->val) {
        return 0;
     }
     bool L = cmp(root1->l, root2->l);
     bool R = cmp(root1->r, root2->r);
     return L & R;
}


bool cmp_tree(tree T1, tree T2) {
    bool ans = cmp(T1.main_root, T2.main_root);
    return ans;
}

int main() {
    /*cin.tie(0);
    cout.tie(0);
    ios::sync_with_stdio(false);*/
    tree T1, T2;
    vector<int> a = {1, 2, 3, 4, 5, 6, 7, 8};
    T1.create(a);
    T1.trav(T1.main_root); cout << "\n";
    int tree_sum = T1.sum_subtree(T1.main_root);
    T1.trav(T1.main_root);
    return 0;
}
