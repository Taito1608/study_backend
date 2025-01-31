// Todoを削除する
async function deleteTodo(todoId) {
    if (!confirm("本当に削除しますか？")) {
        return;
    }

    try {
        const response = await fetch(`/todo/${todoId}`, {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            alert("ToDoを削除しました");
            location.reload();  // ページをリロードして最新のToDoリストを表示
        } else {
            const data = await response.json();
            alert("削除に失敗しました: " + (data.message || "不明なエラー"));
        }
    } catch (error) {
        console.error("エラー:", error);
        alert("エラーが発生しました");
    }
}

