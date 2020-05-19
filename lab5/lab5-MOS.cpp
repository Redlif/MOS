int main()
{
    const int size = 2 * 1024 * 1024; // 2MB
    char* c = (char*)malloc(size);
    for (int i = 0; i < 0xffff; i++) {
        for (int j = 0; j < size; j++) {
            c[j] = i * j;
        }
        std::cout << i << "\n";
    }
}
