
![1](https://user-images.githubusercontent.com/45713796/98271308-d18aac80-1fb5-11eb-9db3-dda942cc1b07.png)


**Kitabe** (*Book in Hindi*) is a Book Recommendation System built for all you Book Lovers📖.
Simply Rate ⭐ some books and get immediate recommendations tailored for you 🤩.<br>
See [Demo](#user-content-demo-) 🎥

[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://kitabe-app.herokuapp.com/)
[![Build Status](https://travis-ci.com/Praful932/Kitabe.svg?token=XKcoN48yFyATXWUZ6d8j&branch=master)](https://travis-ci.com/Praful932/Kitabe) 
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Praful932/Kitabe/blob/master/CONTRIBUTING.md)
[![HitCount](http://hits.dwyl.com/Praful932/Kitabe.svg)](http://hits.dwyl.com/Praful932/Kitabe)
[![GitHub license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) <br>
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Praful932/Kitabe/graphs/commit-activity)
![GitHub stars](https://img.shields.io/github/stars/Praful932/Kitabe?style=social) ![GitHub forks](https://img.shields.io/github/forks/Praful932/Kitabe?style=social) ![GitHub watchers](https://img.shields.io/github/watchers/Praful932/Kitabe?style=social)

# Contents
- [Demo](#user-content-demo-) 🎥
- [Approach](#objective-) 🧐
    - [Objective](#objective-) ✍
    - [Dataset](#dataset-) 🧾
    - [PreProcessing](#preprocessing-) 🛠
    - [Model Exploration](#model-exploration-) 🤯
    - [Final Result](#final-result-) 😁
- [Project Structure](#project-structure-%EF%B8%8F) 💁‍♀️
- [To Do](#to-do-) 🎯
- [Contribute](#contribute-) 🧏‍♂️
- [Notebooks and Files](#notebooks-and-files-) 📓
- [References](#references-) 😇
- [Contributors](#contributors-) 🤗
- [License](#license-) ✍

### Demo 🎥

![kitabe](https://user-images.githubusercontent.com/45713796/98460071-f6a23980-21c6-11eb-881f-ba0f75896751.gif)

### Objective ✍
Our objective is to build an application for all Book Lovers ♥ like us out there where all you have to 
do is rate some of your favorite books and the application will do it's **voodoo magic** 🧙‍♂️ and give you some more books that you may **love😍 to read**.

### Dataset 🧾
The Dataset that we used for this task is the [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) dataset. It consists of 10k books with a total of 6 million ratings. That's huge right! 😮. There are some more huge datasets such as [Book-Crossings](http://www2.informatik.uni-freiburg.de/~cziegler/BX/) but they are kinda old 😬.

**Dataset Structure** 
```
GoodBooks10k 
    ├── books.csv         # Contains book info with book-id                         
    ├── ratings.csv       # Maps user-id to book-id and rating  
    ├── book_tags.csv     # Contains tag-id associated with book-ids
    ├── tags.csv          # Contains tag-name associated with tag-id
    ├── to_read.csv       # Contains book-ids marked as to-read by user  
```

### PreProcessing 🛠
Since this is a recommendation problem, we have to make sure that the `books.csv` is as clean as possible and only consider those ratings whose book-id is present, same goes for vice versa.

More Cleaning for `books.csv`
- Missing Book Image URLs
- Book & Rating Duplicates

### Model Exploration 🤯
For Recommendation Problems there are multiple approaches that are possible:
- Embedding Matrix
- Singular Matrix Decomposition
- Term Frequency

We experimented with several methods and chose Embedding Matrix & Term Frequency.

- **Embedding Matrix** - This method is often called [FunkSVD](https://www.coursera.org/lecture/matrix-factorization/deriving-funksvd-lyTpD) which won the Netflix Prize back in 2004. Since it is a gradient based function minimization approach we like to call it as Embedding Matrix. Calling it SVD [confuses](https://www.quora.com/What-is-the-difference-between-SVD-and-matrix-factorization-in-context-of-recommendation-engine/answer/Luis-Argerich) it with the one in Linear Algebra. This Embedding Matrix constructs a vector for each user and each book, such that when the product is applied with additional constraints it gives us the rating. For more elaborate info on FunkSVD refer [this](http://sifter.org/~simon/journal/20061211.html). 
We used the book embedding as a representation of the books to infer underlying patterns. This led to the embedding able to detect books from the same authors and also infer genres such as Fiction, Autobiography and more.

- **Term Frequency** - This method is like a helper function to above, it shines where embedding fails. Term Frequency takes into account the tokens in a book title be it the book title itself, the name of authors and also rating. Taking into consideration it finds books which match closely with the tokens in the rated book.

> 🛠 Code for every step can be found in the [Notebooks and Files](#notebooks-and-files) Section.

### Final Result 😁
The [Image](https://coggle.it/diagram/X6TOUxlMvSl8FBM4/t/dataset/7083ac4f2de39517a4d97cd9d3d211c11af6e65f9a0034c46d613ff0f9cd5) says it All.

![coggle](https://user-images.githubusercontent.com/45713796/98331008-ae95e200-2021-11eb-915b-892854f88a6e.png)


### Project Structure 💁‍♀️
```
Kitabe
│   
├───BookRecSystem               # Main Project Directory
│       
├───mainapp                     # Project Main App Directory
│   │   
│   └───migrations              # Migrations
│           
├───static          
|   |                           # Static Directory
│   └───mainapp
│       ├───css                 # CSS Files  
|       |                         
│       ├───dataset             # Dataset Files
│       │       
│       ├───gif                 # GIF Media
│       │       
│       ├───model_files         # Model Files
|       |   |      
│       │   ├───surprise        # FunkSVD Files
│       │   │       
│       │   └───cv              # CV Files
│       │           
│       └───png                 # PNG Media FIles
|           
└───templates                   # Root Template DIrectory
    |
    ├───account                 # Account App Templates
    │       
    └───mainapp                 # Project Main App Templates
               
```            

### To Do 🎯
- [ ] Display Top Books Per Week
- [ ] Add AJAX View Tests
- [ ] Add Modal Tests
- [ ] Add User Read Feature
- [ ] Add User To Read Feature
- [ ] Use a Better Approach than Count Vectorizer
- [ ] Better Exhaustive Search For Hyperparameters
- [ ] Add User-User Similarity Recommendations

### Contribute 📝

### Notebooks and Files 📓
- [All Dataset & Model Files](https://drive.google.com/drive/folders/1SvuCvfiSxwuF21EvmKyhSkuwjgK7KU6S?usp=sharing)
- [Cleaning and Embedding Notebook](https://drive.google.com/file/d/1wlKiSvYQEXG7xtru5jDQWQwxffaVd9Ap/view?usp=sharing)
- [Fix Missing Images Notebook](https://drive.google.com/file/d/1S0pd5t9oU9a63EdmlXmxhNWGc228W3ke/view?usp=sharing)
- [Genre Wise & Count Vectorizer Notebook](https://drive.google.com/file/d/1LRr4Nm2I2HRJUTXbRea3sK5A1Bvp_lav/view?usp=sharing)

### References 😇

- [Dataset](https://github.com/zygmuntz/goodbooks-10k)
- [Count Vectorizer](https://www.kaggle.com/sasha18/recommend-books-using-count-tfidf-on-titles)
- [Books2Rec](https://github.com/dorukkilitcioglu/books2rec)

### Contributors 🤗
![2](https://contributors-img.web.app/image?repo=Praful932/Kitabe)

### License ✍
```
MIT License

Copyright (c) 2020 Praful Mohanan & Prajakta Mane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
