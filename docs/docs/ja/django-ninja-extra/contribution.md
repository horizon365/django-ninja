**コントリビューションガイド**
=========

  
NinjaExtra へのコントリビュートをご検討いただきありがとうございます！あなたのコントリビューションは、このプロジェクトをすべての人にとってより良いものにする助けになります。始める前に、以下のガイドラインを一読してください。

  
開発環境のセットアップ
---------

1.    
    リポジトリをフォークする：GitHub 上で NinjaExtra のリポジトリをフォークし、ローカルにクローンします。
    
2.    
    仮想環境：プロジェクト用の仮想環境を作成してアクティベートします。
    
        python -m venv venv
        source venv/bin/activate  # Linux/macOS
        
    
        python -m venv venv
        .\venv\Scripts\activate  # Windows
        
    
3.    
    `flit` のインストール：`flit` がグローバルにインストールされていることを確認します。
    
        pip install flit
        
    
4.    
    依存関係のインストール：開発用ライブラリと pre-commit フックをインストールします。
    
        make install-full
        

### **コードスタイルとフォーマット**

*     
    フォーマット：コードをフォーマットし一貫性を確保するには、次を実行します：
    
        make fmt
        
    
*     
    リント：NinjaExtra はリントに `mypy` と `ruff` を使用しています。コードの構文をチェックするには次のコマンドを実行します：
    
        make lint
        

### **テスト**

*     
    ユニットテスト：ユニットテストには `pytest` を使用しています。テストスイートを実行します：
    
        make test
        
    
*     
    テストカバレッジ：テストカバレッジを確認するには：
    
        make test-cov
        

### **プルリクエストの提出**

1.    
    ブランチ：機能追加やバグ修正用に新しいブランチを作成します。
    
        git checkout -b feature-branch
        
    
2.    
    コミットメッセージ：コミットメッセージは conventional commit 仕様に従ってください。
    
3.    
    変更のプッシュ：ブランチをフォークしたリポジトリにプッシュします。
    
        git push origin feature-branch
        
    
4.    
    プルリクエスト：NinjaExtra リポジトリの `master` ブランチに向けてプルリクエストを開きます。変更内容について明確なタイトルと説明を提供してください。

  
NinjaExtra へのコントリビューションありがとうございます！🚀

<img style="object-fit: cover; object-position: 50% 50%;" alt="relax image for django-ninja.cn" loading="lazy" fetchpriority="auto" aria-hidden="true" draggable="false" src="https://picsum.photos/825/47.jpg">
