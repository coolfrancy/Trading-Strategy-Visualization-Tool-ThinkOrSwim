
def wash(uncleaned_data_path, cleaned_data_path):
    import os
    
    files=os.listdir(uncleaned_data_path)

    # Loop through each file
    for strat in files:
        try:
            # Read the content of the file
            with open(uncleaned_data_path + '/' + strat, 'r', encoding='windows-1252', errors='replace') as rfile:
                old = rfile.readlines()[1:]  # Skip the first line

                #takes out the last three uneeded statements from the data
                for i,line in enumerate(reversed(old)):
                    if 'Max trade' in line:
                        old=old[:-i]

                for i,line in enumerate(old):
                    if ',' in line:
                        old[i]=line.replace(',', '')

                old.pop(1)  # Remove the second line
                old.pop()
                sid = old.pop(3)  # Pop the 4th line (index 3)
                old[0] = old[0].replace('\n', ' ')  # Replace newline in the first line
                old[0] += sid  # Append the SID to the first line


            #make sure the file has enough data
            if len(old)>=3:
                # Now write back to the file
                with open(cleaned_data_path + '/' + strat, 'w', encoding='windows-1252') as wfile:
                    for line in old:
                        if line != '\n':  # Avoid writing empty newlines and stocks without enough trades
                            new_line = line.replace(';', ',')  # Replace semicolons with commas
                            wfile.write(new_line)  # Write the modified line to the file
            else:
                os.remove(uncleaned_data_path + '/' + strat)

        except IndexError:
            os.remove(uncleaned_data_path + '/' + strat)
            continue
        except Exception as e:
            print(f"Error processing {strat}: {e}")
            continue
    

if __name__=='__main__':
    wash('/workspaces/TosChart/TosChart/uncleaned_data', '/workspaces/TosChart/TosChart/cleaned_data')