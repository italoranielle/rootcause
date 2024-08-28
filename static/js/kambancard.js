function kambanAddTask(task){
    const card = document.createElement('div');
    card.className = 'card border-left-success shadow h-100 py-2';
    card.id = `task-${task.pk}`;

    const editIcon = document.createElement('i');
    editIcon.className = 'fas fa-fw fa-pen';

    const editLink = document.createElement('a');
    editLink.className = 'd-flex justify-content-end';
    editLink.href = `/action/task/edit/${task.pk}`

    const deleteIcon = document.createElement('i');
    deleteIcon.className = 'fas fa-fw fa-trash';

    const deleteLink = document.createElement('a');
    deleteLink.className = 'd-flex ml-2 justify-content-end';
    deleteLink.href = `/action/task/delete/${task.pk}`

    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    const header = document.createElement('div');
    header.className = 'px-3 pt-3';

    const options = document.createElement('div');
    options.className = 'row justify-content-end';

    const title =  document.createElement('h5');
    title.innerHTML  = `${task.fields.titulo}`;

    const text = document.createElement('p');
    text.innerHTML  = `${task.fields.oque}`;

    const how = document.createElement('div');
    how.className = 'd-flex justify-content-start px-3 align-items-center pb-2';

    const howicon = document.createElement('div');
    howicon.className = 'fas fa-fw fa-user';

    how.appendChild(howicon);
   // for (const user of task.quem) {
    const username = document.createElement('span');
    username.className = 'quote2 pl-2';
    username.innerHTML  = `${task.fields.quem}`;
    how.appendChild(username);
//}

    const dateContent = document.createElement('div');
    dateContent.className = 'd-flex justify-content-start align-items-center';
    
    const dateicon = document.createElement('i');
    dateicon.className = 'fas fa-fw fa-calendar pl-2';

    const dateStart = document.createElement('span');
    dateStart.className = 'quote2 pl-2';
    dateStart.innerHTML  = `de ${task.fields.quando_inicio}`;

    const dateEnd = document.createElement('span');
    dateEnd.className = 'quote2 pl-2';
    dateEnd.innerHTML  = `ate ${task.fields.quando_fim}`;

    dateContent.appendChild(dateicon);
    dateContent.appendChild(dateStart);
    //dateContent.appendChild(dateicon);
    dateContent.appendChild(dateEnd);
    header.appendChild(title);
    header.appendChild(text);
    editLink.appendChild(editIcon);
    options.appendChild(editLink);
    deleteLink.appendChild(deleteIcon);
    options.appendChild(deleteLink);
    cardBody.appendChild(options);
    cardBody.appendChild(header);
    cardBody.appendChild(how);
    cardBody.appendChild(dateContent);
    card.appendChild(cardBody);

    return card
}


