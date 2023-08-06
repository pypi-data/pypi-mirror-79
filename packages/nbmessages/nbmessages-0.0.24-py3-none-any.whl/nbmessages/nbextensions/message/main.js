define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {
    var tabContent = `
    <div id="nbmessages" class="tab-pane nbmessages">
        <div class="col-sm-2">
            <ul class="nav nav-pills nav-stacked" id="nbmessagess"></ul>
        </div>
        <div class="col-sm-10" id="nbmessage-messages"></div>
    </div>`

    class MessageBoardsPill {
        constructor(appState) {
            $.get(utils.get_body_data('baseUrl') + 'nbmessage/directories', function(data) {
                var directories = JSON.parse(data);
                directories.forEach(function(directory, index) {
                    if (index === 0) {
                        $('#nbmessagess').append(`<li role="presentation" class="nbmessage-pill active"><a href="#">${directory}</a></li>`)
                        appState.updateState({selectedMessageBoard: directory});
                    } else {
                        $('#nbmessagess').append(`<li role="presentation" class="nbmessage-pill"><a href="#">${directory}</a></li>`);
                    }
                });
            
                $('.nbmessage-pill').click(function() {
                    var selectedTabname = $(this).text();
                    appState.updateState({selectedMessageBoard: selectedTabname});
                    that.removeActive();
                    $(this).addClass('active');
                });

            }).fail(function() {});

            this.appState = appState;
            var that = this;


        }

        removeActive() {
            $('.nbmessage-pill').removeClass('active');
        }
    }

    class Messages {
        constructor() {
            this.messagesHTML = undefined;
        }

        update(obj) {
            var messageBoard = obj.selectedMessageBoard;
            var that = this;

            $.get(utils.get_body_data('baseUrl') + 'nbmessage/render/' + messageBoard, function(data) {
                data = JSON.parse(data);

                // only update the html if doesn't match and remove old/append new message
                if (that.messagesHTML !== data.html) {
                    that.messagesHTML = data.html;

                    $('#nbmessage-messages').empty();
                    $('#nbmessage-messages').append(that.messagesHTML);

                    // FIXME dynamic path needs to go somewhere, maybe not here
                    var path = utils.get_body_data('baseUrl');
                    var imgPath = path + 'nbmessage/images/ucsd-0.png';

                    if (!imgPath.startsWith('/')) {
                        imgPath = '/' + imgPath;
                    }

                    $('.img-thumbnail').attr('src', imgPath)
                }   
            }).fail(function() { })
            .catch(function(e) { });
        }

    }

    class MessageState {
        constructor() {
            this.state = {
                selectedMessageBoard: null,
                createCookie: false,
                expirationDate: null,
                cookieValue: null
            }
            this.stateListeners = [];
        }

        updateState(obj, endSet={}) {
            this.state = Object.assign(this.state, obj);
            var that = this;
            this.stateListeners.forEach(function(listener) {
                listener.update(that.state);
            });

            // do a final state update that doesn't inform the listeners after the
            // listeners have been updated
            this.state = Object.assign(this.state, endSet);
        }

        registerStateListener(stateListener) {
            this.stateListeners.push(stateListener)
        }
    }

    class Notification {
        constructor(appState) {
            this.notify = false;
            this.html = `<sup><span><img id="nbmessage-envelope" src="${utils.get_body_data('baseUrl') + 'nbmessage/images/envelope.svg'}"/></span></sup>`;
            this.appState = appState;
        }

        createCookie() {
            var that = this;
            $.get(utils.get_body_data('baseUrl') + 'nbmessage/notify', function(data) {
                data = JSON.parse(data);
                var cookie = new MessageBoardCookie();
                var cookieExists = cookie.exists();
                var cookieValues = cookie.getCookie();
                var cookieId = cookieValues[0];
                var cookieState = cookieValues[1];
    
                if (data.notify && !cookieExists) {
                    // CLEAN CASE, NOTHING HAS BEEN SET: cookie doesn't exist and we want it
                    cookie.setCookie(data.notification_id + '-true', data.expiration_date);
                    that.appendHTML();
                }
                else if (cookieState === 'true') {
                    that.appendHTML();
                }
                else if (data.notify && cookieId !== data.notification_id) {
                    // a NEW notification has been set while the old cookie is still technically active
                    cookie.setCookie(data.notification_id + '-true', data.expiration_date);
                    that.appendHTML();
                }
            })
            .fail(function() { });
        }

        modifyNotification() {
            // click listener
            var that = this;
            $.get(utils.get_body_data('baseUrl') + 'nbmessage/notify', function(data) {
                var cookie = new MessageBoardCookie();
                var cookieValues = cookie.getCookie();
                var cookieId = cookieValues[0];
                cookie.setCookie(cookieId + '-false', data.expiration_date)
                that.removeHTML();
            }).fail(function() {});
        }

        appendHTML() {
            if ($('#nbmessage-envelope').length === 0) {
                $('#nbmessages-tab').append(this.html);
            }
        }

        removeHTML() {
            $('#nbmessage-envelope').remove();
        }

        update(newState) {
            if (newState.clicked) {
                this.modifyNotification();
            }
            this.createCookie();
        }
    }

    class MessageBoardCookie {
    
        setCookie(notifyUser, expirationDate) {
            document.cookie = `nbmessage-notify=${notifyUser}; expires=${expirationDate}`;
        }

        getCookie() {
            var name = 'nbmessage-notify' + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i <ca.length; i++) {
              var c = ca[i];
              while (c.charAt(0) == ' ') {
                c = c.substring(1);
              }
              if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length).split('-');
              }
            }
            return "";
        }

        exists() {
            if (this.getCookie() === '') {
                return false;
            }
            return true;
        }

        remove() {
            document.cookie = `nbmessage-notify=; expires=Thu, 01 Jan 1970 00:00:00 UTC`;
        }

    }

    var load_ipython_extension = function () {
        // add custom css/js
        $('head').append(`<link rel="stylesheet" type="text/css" href="${utils.get_body_data('baseUrl') + 'nbmessage/css/nbmessages.css'}">`);
        $('head').append(`<link rel="stylesheet" type="text/css" href="${utils.get_body_data('baseUrl') + 'nbmessage/css/bootstrap-datepicker.min.css'}">`);

        // set the tab title, everything must take place once the tab is established
        $.get(utils.get_body_data('baseUrl') + 'nbmessage/admin', function(data) {
            var messageState = new MessageState();
            var title = JSON.parse(data);
            $('#tabs').append(`<li ><a href="#nbmessages" id="nbmessages-tab" data-toggle="tab">${title}</a></li>`)
            $('.tab-content').append(tabContent);

           

            // set listener on tab click
            $('#nbmessages-tab').click(function() {
                messageState.updateState({'clicked': true}, endSet={'clicked': false});
            });
            var messageBoardPill = new MessageBoardsPill(messageState);
            var messages = new Messages();
            // var notification = new Notification(messageState);

            messageState.registerStateListener(messages);
            // messageState.registerStateListener(notification);

        }).fail(function() {});
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
