# Auto-Git

### ***pyke elysia***

![only for window](https://img.shields.io/badge/only%20for-window-blue)

### `path.to_current_path()`

目前，同个磁盘中(如：`D:/` -> `D:\dev`)，建议使用相对路径。
而在跨磁盘中(如：`D:/` -> `E:/`)，可以使用绝对路径。

#### 开发原因

由于家中网络问题，不得不多次进行 `git push` 操作，
每次 `push` 失败就要消耗不少于 20 sec 的时间，实在耽搁不起，
而且对于耐心也是一次非常大的挑战。

因此，我选择开发一个简单的，较为自动化的 `git` 操作脚本。

- 一方面

    可以作为一个 `python` 的训练项目。

- 另一方面

    也可以作为可以实实在在使用的一个工具

#

***创建于2025/8/8***