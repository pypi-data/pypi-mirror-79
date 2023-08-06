define(['jquery', 'base/js/utils', './bootstrap-datepicker', 'require'], function ($, utils, require) {

    // following variables define page elements

    // the page components
    var tab = '<li><a href="#nbmessages-admin" data-toggle="tab">nbmessages (Admin)</a></li>';

    var tabContent = `
    <div id="nbmessages-admin" class="tab-pane container nbmessages">
        <div class="col-sm-2" id="nbmessage-nav"></div>
        <div class="col-sm-10" id="nbmessages-admin-content" style="padding-left: 1em"></div>
    </div>`

    class NavPills {
        constructor(appState) {
            this.form = `
            <ul class="nav nav-pills nav-stacked">
                <li role="presentation" id="nbmessage-tab-global" class="active"><a href="#">Global</a></li>
                <li role="presentation" id="nbmessage-tab-messages" ><a href="#">Messages</a></li>
            </ul>
            `

            this.render();
            this.appState = appState;
            $('[role="presentation"]').click(function() {
                var selectedTabname = $(this).text();
                appState.updateState({selectedTab: selectedTabname});
            });
        }

        render() {
            $('#nbmessage-nav').append(this.form);
        }

        removeActive() {
            $('#nbmessage-tab-global').removeClass('active');
            $('#nbmessage-tab-messages').removeClass('active');
        }

        addActive(tabname) {
            switch (tabname) {
                case 'Global':
                    $('#nbmessage-tab-global').addClass('active');
                    break;
                case 'Messages':
                    $('#nbmessage-tab-messages').addClass('active');
                    break;
            }
        }

        update(updatedState) {
            var selectedTab = updatedState.selectedTab;
            this.removeActive();
            this.addActive(selectedTab);
        }
    }

    class GlobalSubform {
        constructor(appState) {
            this.form = `
                <div id="nbmessage-global">
                    <label for="select-message-board">Select a message board to edit</label>
                    <select class="form-control" id="select-message-board" name="select_message_board"></select>
                </div>
            `

            this.appState = appState;

            this.render();
            
            $(document).on('change', '#select-message-board', function() {
                appState.updateState({selectedMessageBoard: $(this).val()})
            });
        }

        render() {
            if ($('#nbmessage-global').length === 0) {
                var that = this;
                $('#nbmessages-admin-content').append(this.form);
                $.get(utils.get_body_data('baseUrl') + 'nbmessage/directories', function(data) {
                    var directories = JSON.parse(data);
                    directories.forEach(function(directory, i) {
                        if (i === 0) {
                            $('#select-message-board').append(`<option selected>${directory}</option>`);
                            that.appState.updateState({selectedMessageBoard: directory});
                        } else {
                            $('#select-message-board').append(`<option>${directory}</option>`);
                        }
                        
                    });
                })
                .fail(function() {});
            }
        }

        remove() {
            $('#nbmessage-global').remove();
        }

        update(updatedState) {
            if (updatedState.selectedTab === 'Global') {
                this.render();
            } else {
                this.remove();
            }
        }
    }

    class MessagesSubform {
        constructor(appState) {
            this.form = `
                <div class="form-group" id="nbmessage-operation-group">
                    <label for="message-operation">Message operation</label>
                    <select class="form-control" id="nbmessage-operation" name="message_operation">
                        <option>Add</option>
                        <option>Delete</option>
                    </select>
                </div>
                <div id="preview-modal" class="modal fade" role="dialog">
                <div class="modal-dialog modal-lg" style="width:60em;">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                            <h4 class="modal-title">Preview</h4>
                            </div>
                            <div class="modal-body"></div>
                            <div class="modal-footer">
                            <button type="button" id='save-message' class="btn btn-default" data-dismiss="modal">Save</button>
                            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="submit-modal" class="modal fade" role="dialog">
                <div class="modal-dialog modal-lg" style="width:60em;">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                            <h4 class="modal-title">Server Response</h4>
                            </div>
                            <div class="modal-body"></div>
                            <div class="modal-footer">
                            <button type="button" id='close-modal' class="btn btn-default" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
            `

            this.addform = `
                <div class="nbmessage-form-group">
                    <form id="nbmessage-admin" method="post">
                        <div class="form-group" id="author">
                            <label for="author">Add your name to the message</label>
                            <input type="text" name="author" class="form-control" placeholder="Your name here" required>
                        </div>

                        <div class="form-group" id="message-id">
                            <label for="message-id">Add a message ID</label>
                            <input type="text" name="message_id" class="form-control" placeholder="message ID here" required>
                        </div>

                        <div class="form-group">
                            <label for="message-body">Add message body (note: must be formatted as a markdown document)</label>
                            <textarea class="form-control" rows="25" name="message_body" required></textarea>
                        </div>

                        <div class="form-check" id="set-notification">
                            <input type="checkbox" class="form-check-input"  name="set_notification">
                            <label class="form-check-label" for="set_notification">Add Notification</label>
                        </div>

                        <div class="form-group">
                            <label for="expiration_date">Set an expiration date for the notification (if applicable)</label>
                            <input type="text" class="form-control" id="datepicker" name="expiration_date">      
                        </div>

                        <div class="form-group">
                            <p>Select a color scheme for footer</p>
                            <select id="color-scheme" class="form-control" name="color_scheme">
                                <option>Default</option>
                                <option>Navy</option>
                                <option>Blue</option>
                                <option>Aqua</option>
                                <option>Teal</option>
                                <option>Olive</option>
                                <option>Green</option>
                                <option>Lime</option>
                                <option>Yellow</option>
                                <option>Orange</option>
                                <option>Red</option>
                                <option>Maroon</option>
                                <option>Fuchsia</option>
                                <option>Purple</option>
                                <option>Black</option>
                                <option>Gray</option>
                                <option>Silver</option>
                            </select>
                        </div>

                        <input name="status" type="hidden" value="preview">
                        <input name="operation" type="hidden" value="add">
                        <input name="base_url" type="hidden" value="${utils.get_body_data('baseUrl')}">
                        <button type="submit" class="btn btn-default">Submit</button>
                    </form>
                </div>
            `

            this.deleteform = `
                <div class="nbmessage-form-group">
                    <form id="nbmessage-admin-delete" method="delete">
                        <div class="nbmessage-form-group">
                            <div class="form-group">
                                <label for="message-operation">Delete a message</label>
                                <select class="form-control" id="delete-message" name="message_id"></select>
                            </div>
                            <div id="nbmessage-rendered"></div>
                        </div>
                        <br/>
                        <input name="operation" type="hidden" value="delete">
                        <br/>
                        <button type="submit" class="btn btn-default">Submit</button>
                    </form>
                </div>
            `

            this.selectedMessageBoard;
            this.messageOperation;
            this.appState = appState;

        }

        render() {
            if ($('#nbmessage-operation-group').length === 0) {
                $('#nbmessages-admin-content').append(this.form);
                this.showSubform(this.messageOperation);
                
                // event listeners are dependent on whether element exists in render step
                var that = this;
                $('#nbmessage-operation').change(function() {
                    that.appState.updateState({messageOperation: $(this).val()})
                });
            }
        }

        remove() {
            // empty?
            $('#nbmessage-operation-group').remove(); 
            $('.nbmessage-form-group').remove();
        }

        setupFormDelete() {
            var that = this;
            $('#nbmessage-admin-delete').off('submit');
            $('#save-message').off('click');

            $('#nbmessage-admin-delete').submit(function(event) {
                event.preventDefault();
                var form = $(this);
                var rawFormData = form.serializeArray();
                var formData = {};
                $(rawFormData).each(function(index, obj){
                    formData[obj.name] = obj.value;
                });

                $('.modal-body').empty();
                $('.modal-body').append(`<p class="alert alert-warning">Are you sure you want to delete message ID = ${formData.message_id}?</p>`);
                $('#preview-modal').modal('show');

                $('#save-message').click(function() {
                    $.ajax({
                        type: form.attr('method'),
                        url: utils.get_body_data('baseUrl') + `nbmessage/messages/${that.selectedMessageBoard}`,
                        headers: {'X-CSRFToken': getCookie("_xsrf")},
                        data: JSON.stringify(formData)
                        // data: form.serialize()
                    }).done(function(template) {
                        // Optionally alert the user of success here...
                        $('#close-modal, .close').off();
                        $('.modal-body').empty();
                        $('.modal-body').append(template);
                        $('#submit-modal').modal('show');

                        $('#close-modal, .close').click(function() {
                            window.location.reload();
                        })
    
                        // launch modal
                    }).fail(function(err) {
                        // Optionally alert the user of an error here...
                        $('.modal-body').empty();
                        $('.modal-body').append(`<p class="alert alert-warning">${err.responseText}</p>`);
                        $('#preview-modal').modal('show');
                    });
                });
            });
        }

        setupFormSubmit() {
            var that = this;
            // remove event handlers that may be lingering
            $('#nbmessage-admin').off();
            $('#save-message').off();


            $('#nbmessage-admin').submit(function(event) {
        
                event.preventDefault();
                event.stopImmediatePropagation();
                var form = $(this);
    
                var rawFormData = form.serializeArray();
                var formData = {};
                $(rawFormData).each(function(index, obj){
                    formData[obj.name] = obj.value;
                });
                
                // PREVIEW SUBMIT
                $.ajax({
                    type: form.attr('method'),
                    url: utils.get_body_data('baseUrl') + `nbmessage/messages/${that.selectedMessageBoard}`,
                    headers: {'X-CSRFToken': getCookie("_xsrf")},
                    data: JSON.stringify(formData)
                    // data: form.serialize()
                  }).done(function(template) {
                    // Optionally alert the user of success here...
                    $('.modal-body').empty();
                    $('.modal-body').append(template);
                    $('.modal-footer >p').remove();
                    $('.modal-footer').prepend(`<p class="col-sm-6" style="padding: 0; margin: 0;">The above message will be published to message board = ${that.selectedMessageBoard}</p>`);
                    $('#preview-modal').modal('show');
                    $('#save-message').off(); // KEEP THIS, will prevent multiple submits fromt aking place

                    // SUBMITTED MESSAGE
                    $('#save-message').click(function() {
                        formData.status = 'submit';
                        formData.operation = 'add';
                        $.ajax({
                            type: form.attr('method'),
                            url: utils.get_body_data('baseUrl') + `nbmessage/messages/${that.selectedMessageBoard}`,
                            headers: {'X-CSRFToken': getCookie("_xsrf")},
                            data: JSON.stringify(formData)
                        }).done(function(responseMessage) {
                            // success modal
                            $('#close-modal').off();
                            $('.modal-body').empty();
                            $('.modal-footer >p').remove();
                            $('.modal-body').append(`<p class="alert alert-success">${responseMessage}</p>`);
                            $('#submit-modal, .close').modal('show');
                            $('#close-modal').click(function() {
                                window.location.reload();
                            });

                        }).fail(function(err) {
                            // failure modal, could not save or something
                            $('.modal-body').empty();
                            $('.modal-body').append(`<p class="alert alert-danger">${err.responseText}</p>`);
                            $('#submit-modal').modal('show');

                        }).always(function() {
                            $('.modal-footer > p').remove();
                        });
                    });

                    // launch modal
                  }).fail(function(err) {
                    // Optionally alert the user of an error here...
                    $('.modal-body').empty();
                    $('.modal-body').append(`<p class="alert alert-warning">${err.responseText}</p>`);
                    $('#preview-modal').modal('show');
                });
            
            });
        }

        getDeleteInfo() {
            var that = this;
            $.get(utils.get_body_data('baseUrl') + `nbmessage/messages/${this.selectedMessageBoard}`, function(data) {
                var messageInfo = JSON.parse(data);
                var messageInfoLength = Object.keys(messageInfo).length;

                var i = 0;
                for (var messageId in messageInfo) {
                    if (i === messageInfoLength - 1) {
                        $('#delete-message').append(`<option selected>${messageId}</option>`);
                        that.addDeleteMessage(messageInfo, messageId);
                    } else {
                        $('#delete-message').append(`<option>${messageId}</option>`);
                    }
                    i++;
                }

                $(document).on('change', '#delete-message>select', function() {
                    var selectedMessageId = $(this).val();
                    that.addDeleteMessage(messageInfo, selectedMessageId);
                })
                .fail(function() {});
            });
        }

        addDeleteMessage(messageInfo, messageId) {
            var body = messageInfo[messageId];
            $('#nbmessage-rendered').empty();
            $('#nbmessage-rendered').append(body);
        }

        showSubform(messageOperation) {
            // remove the existing subform and render selected one
            $('.nbmessage-form-group').remove();
    
            switch(messageOperation) {
                case 'Add':
                    $('#nbmessage-operation-group').after(this.addform);
                    $('#datepicker').datepicker('getFormattedDate');    
                    this.setupFormSubmit();
                    break;

                case 'Delete':
                    $('#nbmessage-operation-group').after(this.deleteform);
                    this.getDeleteInfo();
                    this.setupFormDelete();
                    break;
            }
        }

        update(updatedState) {
            // update message board
            if (Object.keys(updatedState).indexOf('selectedMessageBoard') > -1) {
                this.selectedMessageBoard = updatedState.selectedMessageBoard;
            }

            // render the view or not
            if (updatedState.selectedTab === 'Messages') {
                this.render();
            } else {
                this.remove();
            }

            // operation selected
            this.messageOperation = updatedState.messageOperation;
            this.showSubform(this.messageOperation);
        }
    }

    class AppState {
        constructor() {
            this.state = {
                selectedMessageBoard: null,
                messageIdPreview: null,
                selectedTab: 'Global',
                messageOperation: 'Add'
            }

            this.stateListeners = []
        }  

        updateState(obj) {
            this.state = Object.assign(this.state, obj);
            var that = this;
            this.stateListeners.forEach(function(listener) {
                listener.update(that.state);
            });
        }

        registerStateListener(stateListener) {
            this.stateListeners.push(stateListener)
        }

    }

    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }

    var load_ipython_extension = function () {
        
        // Add Main Components
        $('#tabs').append(tab);
        $('.tab-content').append(tabContent);

        /** Class initializations */
        var appState = new AppState();

        var globalSubform = new GlobalSubform(appState);
        var navPills = new NavPills(appState);
        var messagesSubform = new MessagesSubform(appState);
        /**  Initialization data retrievals and updates */
        
        // setup the appState object, used as a command pattern to update state for all registered objects
        appState.registerStateListener(navPills);
        appState.registerStateListener(globalSubform);
        appState.registerStateListener(messagesSubform);

        // get the title
        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var title = JSON.parse(data);
            $('#tab-title>input').attr("placeholder", title)
        })
        .fail(function() {});
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
