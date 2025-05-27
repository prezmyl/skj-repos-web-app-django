from graphviz import Digraph
from IPython.display import Image, display

# Create an ER diagram with all fields
dot = Digraph('ERD', format='png')
dot.attr(rankdir='LR', size='8,5')

# Define nodes (tables) with fields
dot.node('User', 'User\n- id PK\n- username\n- email\n- ...')
dot.node('Repository', 'Repository\n- id PK\n- owner_id FK\n- name\n- description\n- is_private\n- created_at')
dot.node('Commit', 'Commit\n- id PK\n- repository_id FK\n- author_id FK\n- message\n- hash\n- timestamp')
dot.node('Label', 'Label\n- id PK\n- name\n- color')
dot.node('Issue', 'Issue\n- id PK\n- repository_id FK\n- author_id FK\n- title\n- description\n- is_open\n- created_at\n- updated_at')
dot.node('Comment', 'Comment\n- id PK\n- issue_id FK\n- author_id FK\n- content\n- created_at')
dot.node('PullRequest', 'PullRequest\n- id PK\n- repository_id FK\n- author_id FK\n- title\n- description\n- source_branch\n- target_branch\n- is_merged\n- created_at\n- updated_at')

# Define relationships
dot.edge('User', 'Repository', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('Repository', 'Commit', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('User', 'Commit', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('Repository', 'Issue', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('User', 'Issue', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('Issue', 'Comment', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('User', 'Comment', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('Repository', 'PullRequest', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('User', 'PullRequest', label='1:N', arrowhead='none', arrowtail='crow')
dot.edge('Issue', 'Label', label='M:N', arrowhead='crow', arrowtail='crow')

# Render diagram to file and display it
output_path = '/mnt/data/erd'
dot.render(filename=output_path)
display(Image(filename=output_path + '.png'))
